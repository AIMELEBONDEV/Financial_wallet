import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import yaml
import logging
import time

# ==============================
# LOGGING
# ==============================
log_path = Path("data/logs/fetch_daily.log")
log_path.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# ==============================
# CHARGER LES TICKERS
# ==============================
def load_tickers(yaml_file="config/tickers.yaml"):
    yaml_path = Path(yaml_file)
    if not yaml_path.exists():
        raise FileNotFoundError(f"❌ Fichier YAML introuvable : {yaml_path.resolve()}")

    with open(yaml_path, "r") as f:
        config = yaml.safe_load(f)

    tickers = []
    for category in ["stocks", "indices", "cryptos"]:
        if category in config:
            for item in config[category]:
                tickers.append({
                    "symbol": item["ticker"],
                    "name": item["name"],
                    "category": category
                })
    return tickers

# ==============================
# TÉLÉCHARGER LES DONNÉES
# ==============================
def fetch_ticker_data(ticker_info, start_date, end_date=None, max_retries=3, sleep_retry=10):
    ticker = ticker_info["symbol"]
    name = ticker_info.get("name", ticker)

    end_date = end_date or datetime.today()

    for attempt in range(1, max_retries + 1):
        try:
            print(f"{ticker}: téléchargement depuis {start_date.date()} → {end_date.date()}")
            ticker_obj = yf.Ticker(ticker)
            df = ticker_obj.history(
                start=start_date.strftime("%Y-%m-%d"),
                end=end_date.strftime("%Y-%m-%d"),
                interval="1d"
            )

            if df.empty:
                raise ValueError("DataFrame vide renvoyé par yfinance")

            df.reset_index(inplace=True)

            # Normaliser colonnes
            df = df.rename(columns={
                "Date": "Date",
                "Open": "Open",
                "High": "High",
                "Low": "Low",
                "Close": "Close",
                "Volume": "Volume"
            })

            # Ajouter colonnes metadata
            df["Ticker"] = ticker
            df["Name"] = name
            df["Category"] = ticker_info.get("category")

            df = df[["Ticker", "Name", "Category", "Date", "Open", "High", "Low", "Close", "Volume"]]

            return df

        except Exception as e:
            if "Too Many Requests" in str(e):
                wait = 60
                print(f"⏳ Rate limit atteint pour {ticker}, pause {wait}s...")
                time.sleep(wait)
            else:
                print(f"⚠️ Tentative {attempt}/{max_retries} échouée pour {ticker}: {e}")
                time.sleep(sleep_retry)

    print(f"❌ Échec définitif : {ticker}")
    return pd.DataFrame()

# ==============================
# MAIN
# ==============================
def main(years_back=5, sleep_between=10):
    tickers = load_tickers()

    out_dir = Path("data/parquet")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "daily_data.parquet"

    # Charger l’existant si dispo
    if out_path.exists():
        df_all = pd.read_parquet(out_path)
        print(f"📂 Parquet existant trouvé ({len(df_all)} lignes)")
    else:
        df_all = pd.DataFrame()

    new_dfs = []

    for t_info in tickers:
        ticker = t_info["symbol"]

        if not df_all.empty and ticker in df_all["Ticker"].unique():
            last_date = df_all.loc[df_all["Ticker"] == ticker, "Date"].max()
            start_date = pd.to_datetime(last_date) + timedelta(days=1)
        else:
            start_date = datetime.today() - timedelta(days=years_back * 365)

        # Vérifie si on est déjà à jour
        if start_date.date() > datetime.today().date():
            print(f"✅ {ticker} déjà à jour (jusqu’à {last_date.date()})")
            continue

        df_ticker = fetch_ticker_data(t_info, start_date=start_date)

        if not df_ticker.empty:
            new_dfs.append(df_ticker)
            print(f"📈 {ticker}: {len(df_ticker)} nouvelles lignes")
        else:
            print(f"❌ {ticker}: pas de nouvelles données")

        time.sleep(sleep_between)

    # Ajouter les nouvelles données
    if new_dfs:
        df_all = pd.concat([df_all] + new_dfs, ignore_index=True)
        df_all.drop_duplicates(subset=["Ticker", "Date"], inplace=True)

        df_all.to_parquet(out_path, index=False)
        print(f"\n✅ Données mises à jour → {out_path} ({len(df_all)} lignes)")
    else:
        print("⏸ Rien de nouveau à ajouter.")

if __name__ == "__main__":
    main(years_back=5, sleep_between=10)

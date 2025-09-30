# scripts/info_data.py
import yfinance as yf
import pandas as pd
import time
from pathlib import Path
import yaml

# Configuration
yaml_path = Path("config/tickers.yaml")
sleep_sec = 30  # pause entre chaque ticker
pause_every = 3  # pause globale après ce nombre de tickers
retry_max = 3    # nombre de tentatives max par ticker

# Charger les tickers
with open(yaml_path, "r") as f:
    data_yaml = yaml.safe_load(f)

tickers_list = []
for category in ["stocks", "indices", "cryptos"]:
    if category in data_yaml:
        tickers_list.extend(data_yaml[category])

print(f"{len(tickers_list)} tickers trouvés dans {yaml_path}")

all_metadata = []

for idx, t_info in enumerate(tickers_list):
    ticker = t_info["ticker"]
    print(f"Récupération metadata pour {ticker}...")

    success = False
    for attempt in range(1, retry_max + 1):
        try:
            ticker_obj = yf.Ticker(ticker)
            info = ticker_obj.info

            # Ajouter quelques infos pertinentes
            metadata = {
                "ticker": ticker,
                "name": t_info.get("name"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "country": info.get("country"),
                "marketCap": info.get("marketCap"),
                "fullTimeEmployees": info.get("fullTimeEmployees"),
                "currency": info.get("currency"),
                "quoteType": info.get("quoteType")
            }

            all_metadata.append(metadata)
            print(f"Metadata récupérées pour {ticker}")
            success = True
            break

        except Exception as e:
            wait = sleep_sec * attempt * 2
            print(f"Tentative {attempt}/{retry_max} échouée pour {ticker} : {e}. Attente {wait}s...")
            time.sleep(wait)

    if not success:
        print(f"Abandon pour {ticker}")

    # Pause entre tickers
    time.sleep(sleep_sec)

    # Pause globale tous les `pause_every` tickers
    if (idx + 1) % pause_every == 0:
        print("Pause de 60s pour éviter le blocage Yahoo Finance...")
        time.sleep(60)

# Sauvegarder parquet
if all_metadata:
    out_dir = Path("data/processed")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "metadata.parquet"

    df_meta = pd.DataFrame(all_metadata)
    df_meta.to_parquet(out_path, index=False)
    print(f"Metadata sauvegardées → {out_path} ({len(df_meta)} lignes)")
else:
    print("Aucun metadata récupéré. Réessaye plus tard.")

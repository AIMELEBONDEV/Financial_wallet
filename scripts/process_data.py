# scripts/process_data.py
import pandas as pd
import numpy as np
from pathlib import Path

# === Config ===
INPUT_FILE = "data/parquet/daily_data.parquet"
OUTPUT_FILE = "data/processed/portfolio_enriched.parquet"
BENCHMARK = "^GSPC"  # Indice de référence pour beta/alpha

# === Fonctions ===
def enrich(df, benchmark_returns=None):
    df = df.sort_values("date").copy()

    # Rendements
    df["daily_return"] = df["adj_close"].pct_change()
    df["cumulative_return"] = (1 + df["daily_return"]).cumprod()

    # Volatilité
    df["volatility_20d"] = df["daily_return"].rolling(20).std()

    # Moyennes mobiles
    df["rolling_mean_50"] = df["adj_close"].rolling(50).mean()
    df["rolling_mean_200"] = df["adj_close"].rolling(200).mean()

    # Drawdown
    df["cummax"] = df["cumulative_return"].cummax()
    df["drawdown"] = df["cumulative_return"] / df["cummax"] - 1
    df["max_drawdown"] = df["drawdown"].cummin()

    # Sharpe (rolling 20j, taux sans risque = 0)
    rolling_mean = df["daily_return"].rolling(20).mean()
    rolling_std = df["daily_return"].rolling(20).std()
    df["sharpe_20d"] = rolling_mean / rolling_std

    # Sortino (rolling 20j)
    downside_std = df["daily_return"].where(df["daily_return"] < 0).rolling(20).std()
    df["sortino_20d"] = rolling_mean / downside_std

    # Beta & Alpha (si benchmark dispo)
    if benchmark_returns is not None:
        cov = df["daily_return"].rolling(60).cov(benchmark_returns)
        var = benchmark_returns.rolling(60).var()
        df["beta_60d"] = cov / var
        df["alpha_60d"] = df["daily_return"].rolling(60).mean() - df["beta_60d"] * benchmark_returns.rolling(60).mean()
    else:
        df["beta_60d"] = np.nan
        df["alpha_60d"] = np.nan

    return df

# === Script principal ===
def main():
    # Charger données
    df = pd.read_parquet(INPUT_FILE)

    # Harmoniser noms de colonnes : minuscule + standardiser adj_close
    df.columns = [col.lower().replace(" ", "_") for col in df.columns]

    # Vérifier que la colonne adj_close existe
    if "adj_close" not in df.columns:
        if "close" in df.columns:
            df = df.rename(columns={"close": "adj_close"})
        else:
            raise KeyError("Impossible de trouver la colonne 'Adj Close' ou 'Close' dans le parquet")

    print(f"✅ Données chargées : {df['ticker'].nunique()} tickers, {len(df)} lignes")

    # Préparer benchmark
    benchmark_df = df[df["ticker"] == BENCHMARK].sort_values("date")
    benchmark_returns = benchmark_df["adj_close"].pct_change() if not benchmark_df.empty else None

    # Appliquer enrichissement par ticker
    all_dfs = []
    for ticker, df_ticker in df.groupby("ticker"):
        df_enriched = enrich(df_ticker, benchmark_returns)
        all_dfs.append(df_enriched)

    df_final = pd.concat(all_dfs, ignore_index=True)

    # Sauvegarder
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    df_final.to_parquet(OUTPUT_FILE, index=False)
    print(f"💾 Données enrichies sauvegardées → {OUTPUT_FILE} ({len(df_final)} lignes)")

if __name__ == "__main__":
    main() 

import yfinance as yf
import pandas as pd
import numpy as np

# === Investor Inputs ===
investment_horizon = "Mid-term"   # Options: Short-term, Mid-term, Long-term
risk_appetite = "Moderate"        # Options: Low, Moderate, High

# === Economic Stage (manual for now) ===
macro_stage = "Expansion"  # Options: Recession, Recovery, Expansion

# === Sector Mapping by Economic Stage ===
sector_map = {
    "Expansion": ["Financials", "IT", "Consumer Goods"],
    "Recession": ["Pharma", "FMCG", "Utilities"],
    "Recovery": ["Industrials", "Auto", "Infra"]
}
selected_sectors = sector_map.get(macro_stage, [])

# === NSE Stock Pool by Sector ===
stocks_by_sector = {
    "IT": ["INFY.NS", "TCS.NS", "WIPRO.NS"],
    "Financials": ["HDFCBANK.NS", "ICICIBANK.NS", "KOTAKBANK.NS"],
    "Consumer Goods": ["ASIANPAINT.NS", "BRITANNIA.NS", "HINDUNILVR.NS"],
    "Pharma": ["SUNPHARMA.NS", "CIPLA.NS", "DIVISLAB.NS"],
    "FMCG": ["HINDUNILVR.NS", "ITC.NS", "DABUR.NS"],
    "Utilities": ["POWERGRID.NS", "NTPC.NS", "RELIANCE.NS"],
    "Industrials": ["LT.NS", "SIEMENS.NS", "BEL.NS"],
    "Auto": ["TATAMOTORS.NS", "EICHERMOT.NS", "BAJAJ-AUTO.NS"],
    "Infra": ["IRCTC.NS", "NBCC.NS", "ADANIPORTS.NS"]
}

# === Compile All Relevant Stocks ===
selected_stocks = []
for sector in selected_sectors:
    selected_stocks.extend(stocks_by_sector.get(sector, []))

# === Market Constants ===
risk_free_rate = 0.07
market_return = 0.12
market_risk_premium = market_return - risk_free_rate

# === Final Filtered Stock List ===
final_results = []

for symbol in selected_stocks:
    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        roic = info.get("returnOnEquity", np.nan)  # Used as a proxy for ROIC
        beta = info.get("beta", 1)
        coe = risk_free_rate + beta * market_risk_premium

        fcf = info.get("freeCashflow", np.nan)
        market_cap = info.get("marketCap", np.nan)
        fcf_yield = fcf / market_cap if fcf and market_cap else np.nan

        if roic and roic > coe and fcf_yield and fcf_yield > 0.03:
            final_results.append({
                "Stock": symbol,
                "ROIC (%)": round(roic * 100, 2),
                "Cost of Equity (%)": round(coe * 100, 2),
                "FCF Yield (%)": round(fcf_yield * 100, 2),
                "Beta": round(beta, 2)
            })

    except Exception:
        continue

# === Display Final Table ===
df = pd.DataFrame(final_results)
df.sort_values(by="ROIC (%)", ascending=False, inplace=True)
print(df.to_string(index=False))
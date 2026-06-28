"""
Download and process financial market data from Yahoo Finance.
"""

from pathlib import Path
import pandas as pd
import yfinance as yf

def download_oil_data(start_date: str, end_date: str) -> pd.DataFrame:
    """Download historical Brent and WTI oil futures data from yfinance."""

    tickers = ["BZ=F", "CL=F"]  # Brent and WTI futures tickers

    data = yf.download(
        tickers, 
        start=start_date, 
        end=end_date,
        auto_adjust=False,
    )

    return data

def create_weekly_oil_features(data: pd.DataFrame) -> pd.DataFrame:
    """Create weekly close, average close, and return features for Brent and WTI oil futures."""

    brent_close = data["Close"]["BZ=F"]
    wti_close = data["Close"]["CL=F"]

    brent_weekly_close = brent_close.resample("W").last()
    wti_weekly_close = wti_close.resample("W").last()

    brent_weekly_avg = brent_close.resample("W").mean()
    wti_weekly_avg = wti_close.resample("W").mean()

    features = pd.DataFrame({
        "Week": brent_weekly_close.index,
        "Brent_Close": brent_weekly_close.values,
        "Brent_Avg_Close": brent_weekly_avg.values,
        "Brent_Return": brent_weekly_close.pct_change().values,
        "WTI_Close": wti_weekly_close.values,
        "WTI_Avg_Close": wti_weekly_avg.values,
        "WTI_Return": wti_weekly_close.pct_change().values,
    })


    # Clean display and output
    numeric_cols = [
        "Brent_Close", 
        "Brent_Avg_Close", 
        "Brent_Return", 
        "WTI_Close", 
        "WTI_Avg_Close", 
        "WTI_Return"
    ]

    features[numeric_cols] = features[numeric_cols].round(4)

    return features

def save_financial_features(df: pd.DataFrame, output_path: str) -> None:
    """Save the financial features DataFrame to a CSV file."""

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_file, index=False)

    print(f"Saved financial features to {output_file}")
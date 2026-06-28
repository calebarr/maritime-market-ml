"""
Merge AIS weekly port features with financial weekly features.
"""

from pathlib import Path
import pandas as pd

# Weeks of delay between shipping activity and oil market response.
# Change this to test different lag periods.
LAG_WEEKS = 3

def load_csv(path: str) -> pd.DataFrame:
    """Load a CSV file into a DataFrame."""

    return pd.read_csv(path)

def merge_ais_financial_data(
    ais_path: str, 
    financial_path:str
) -> pd.DataFrame:
    """Merge AIS weekly port features with financial weekly features on Week."""

    ais_df = load_csv(ais_path)
    financial_df = load_csv(financial_path)

    financial_df = create_lagged_financial_targets(
        financial_df, 
        lag_weeks=LAG_WEEKS
    )

    ais_df["Week"] = pd.to_datetime(ais_df["Week"])
    financial_df["Week"] = pd.to_datetime(financial_df["Week"])

    merged_df = ais_df.merge( 
        financial_df, 
        on="Week", 
        how="inner"
    )

    return merged_df

def create_lagged_financial_targets(
    df: pd.DataFrame, 
    lag_weeks: int = LAG_WEEKS
) -> pd.DataFrame:
    """Create future financial target columns before merging."""

    df = df.copy()

    target_cols = [
        "Brent_Close", 
        "Brent_Avg_Close", 
        "Brent_Return", 
        "WTI_Close", 
        "WTI_Avg_Close", 
        "WTI_Return"
    ]   

    for col in target_cols:
        df[f"{col}_Next{lag_weeks}W"] = df[col].shift(-lag_weeks)

    return df

def save_merged_data(df: pd.DataFrame, output_path: str) -> None:
    """Save the merged DataFrame to a CSV file."""

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_file, index=False)

    print(f"Merged data saved to {output_file}")
    print(f"Rows: {len(df)}") 
    print(f"Columns: {len(df.columns)}")


def main() -> None:
    """Run the merge pipeline"""

    ais_path = "/Users/calebarrivillaga/Library/CloudStorage/GoogleDrive-calebar@umich.edu/My Drive/maritime-market-ml/cleaned_data/ais_weekly_port_features_master.csv"
    financial_path = "/Users/calebarrivillaga/Library/CloudStorage/GoogleDrive-calebar@umich.edu/My Drive/maritime-market-ml/cleaned_data/financial_weekly_features_master.csv"
    
    lagged_output = f"/Users/calebarrivillaga/Library/CloudStorage/GoogleDrive-calebar@umich.edu/My Drive/maritime-market-ml/merged_data/merged_{LAG_WEEKS}W.csv"

    print("Starting AIS + financial merge")

    merged_data = merge_ais_financial_data(
        ais_path=ais_path, 
        financial_path=financial_path
    )
    
    save_merged_data(
        merged_data, 
        output_path=lagged_output
    )

    print("Merge pipeline completed successfully.")

if __name__ == "__main__":
    main()
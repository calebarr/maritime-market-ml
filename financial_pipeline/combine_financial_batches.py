"""
Combine multiple financial batch files into a single DataFrame.
"""

from pathlib import Path
import pandas as pd

def combine_financial_batches(
        batch_dir: str, 
        output_path: str
) -> pd.DataFrame:
    """Combine financial batch files into a master weekly dataset."""

    batch_path = Path(batch_dir)

    csv_files = sorted(
        batch_path.glob("financial_weekly_*.csv")
    )

    if not csv_files:
        raise ValueError(
            f"No batch CSV files found in {batch_dir}"
        )
    
    df_list = []

    for csv_file in csv_files:
        print(f"Loading batch file {csv_file.name}...")

        df = pd.read_csv(csv_file)

        df["Week"] = pd.to_datetime(
            df["Week"], 
            errors="coerce"
        )

        df_list.append(df)

    combined_df = pd.concat(df_list, ignore_index=True)

    master = (
        combined_df.sort_values("Week")
        .drop_duplicates(subset="Week", keep="last")
        .reset_index(drop=True)
    )

    numeric_cols = [
        "Brent_Close",
        "Brent_Avg_Close",
        "Brent_Return",
        "WTI_Close",
        "WTI_Avg_Close",
        "WTI_Return",
    ]

    master[numeric_cols] = master[numeric_cols].round(4)

    master = master.sort_values("Week").reset_index(drop=True)

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    master.to_csv(output_file, index=False)

    print(f"Saved master financial weekly features to {output_file}")
    print(f"Rows: {len(master)}")
    print(f"Columns: {len(master.columns)}")
    print(f"Weeks: {master['Week'].nunique()}")

    return master

def main() -> None:
    """Run the financial batch combine pipeline."""

    batch_dir = (
        "/Users/calebarrivillaga/Library/CloudStorage/"
        "GoogleDrive-calebar@umich.edu/My Drive/"
        "maritime-market-ml/cleaned_data/"
        "financial_batches"
    )
    output_path = (
        "/Users/calebarrivillaga/Library/CloudStorage/"
        "GoogleDrive-calebar@umich.edu/My Drive/"
        "maritime-market-ml/cleaned_data/"
        "financial_weekly_features_master.csv"
    )

    print("Starting financial batch combine pipeline...")
    
    combine_financial_batches(
        batch_dir=batch_dir,
        output_path=output_path
    )

    print("Financial batch combine completed successfully!")

if __name__ == "__main__":
    main()

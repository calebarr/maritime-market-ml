"""
Combine multiple AIS batch files into a single DataFrame.
"""

from pathlib import Path
import pandas as pd

def combine_ais_batches(batch_dir: str, output_path: str) -> pd.DataFrame:
    """Combine multiple AIS batch files and resolve overlapping weekly port rows."""

    batch_path = Path(batch_dir)
    csv_files = sorted(batch_path.glob("ais_weekly*.csv"))

    if not csv_files:
        raise ValueError(f"No batch CSV files found in {batch_dir}")
    
    df_list = []

    for csv_file in csv_files:
        print(f"Loading batch file {csv_file.name}...")
        df = pd.read_csv(csv_file)
        df["Week"] = pd.to_datetime(df["Week"], errors="coerce")
        df_list.append(df)

    combined_df = pd.concat(df_list, ignore_index=True)

    master = (
        combined_df.groupby(["Week", "Port"], as_index=False)
        .agg(
            Tanker_Vessels=("Tanker_Vessels", "sum"),
            Cargo_Vessels=("Cargo_Vessels", "sum"),
            Draft=("Draft", "mean"),
            Avg_SOG=("Avg_SOG", "mean"),
            Avg_Length=("Avg_Length", "mean"),
            Unique_Vessels=("Unique_Vessels", "sum"),
        )
    )

    numeric_cols = [
        "Draft",
        "Avg_SOG",
        "Avg_Length",
    ]

    master[numeric_cols] = master[numeric_cols].round(2)

    master = master.sort_values(["Week", "Port"]).reset_index(drop=True)

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    master.to_csv(output_file, index=False)

    print(f"Saved master AIS weekly port features to {output_file}")
    print(f"Rows: {len(master)}")
    print(f"Columns: {len(master.columns)}")
    print(f"Week: {master['Week'].nunique()}")
    print(f"Ports: {master['Port'].nunique()}")

    return master

def main() -> None:
    """Run the AIS batch combine pipeline."""

    batch_dir = (
        "/Users/calebarrivillaga/Library/CloudStorage/"    
        "GoogleDrive-calebar@umich.edu/My Drive/" 
        "maritime-market-ml/cleaned_data/ais_batches"
    )

    output_path = (
        "/Users/calebarrivillaga/Library/CloudStorage/"
        "GoogleDrive-calebar@umich.edu/My Drive/"
        "maritime-market-ml/cleaned_data/ais_weekly_port_features_master.csv"
    )

    print("Starting AIS batch combine pipeline...")

    combine_ais_batches(
        batch_dir=batch_dir,
        output_path=output_path
    )

    print("AIS batch combine pipeline completed successfully!")
    
if __name__ == "__main__":
    main()

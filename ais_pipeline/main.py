"""
Main entry point for this AIS data processing pipeline
"""
import sys
from pathlib import Path

from downloader import download_ais_data
from processor import (
    process_all_zip_files,
    load_processed_csv_files,
    extract_first_arrivals_anywhere,
    create_port_activity_features,
)
from plotting import create_first_arrivals_map



def main() -> None:
    """Run the AIS pipeline"""

    # Expect arguments from terminal
    if len(sys.argv) != 3:
        print(
            "Usage: python main.py <start_date> <end_date>"
        )
        sys.exit(1)

    start_date = sys.argv[1]
    end_date = sys.argv[2]

    # Google Cloud Storage bucket paths for raw and processed data
    raw_data_dir = "/Users/calebarrivillaga/Library/CloudStorage/GoogleDrive-calebar@umich.edu/My Drive/maritime-market-ml/raw_data/ais"
    processed_data_dir = (
        "/Users/calebarrivillaga/Library/CloudStorage/"
        "GoogleDrive-calebar@umich.edu/My Drive/"
        "maritime-market-ml/cleaned_data/"
        "processed_batches/"
        f"processed_{start_date}_to_{end_date}"
    )
    output_html = "/Users/calebarrivillaga/Library/CloudStorage/GoogleDrive-calebar@umich.edu/My Drive/maritime-market-ml/outputs/first_arrivals_map.html"

    batch_output_dir = "/Users/calebarrivillaga/Library/CloudStorage/GoogleDrive-calebar@umich.edu/My Drive/maritime-market-ml/cleaned_data/ais_batches"

    feature_output = (
        f"{batch_output_dir}/"
        f"ais_weekly_{start_date}_to_{end_date}.csv"    
    )

    # Step 1 - download AIS data
    download_ais_data(
        start_date=start_date,
        end_date=end_date,
        save_dir=raw_data_dir
    )

    # Step 2 - load raw AIS files
    print("Processing raw AIS zip files...")
    process_all_zip_files(raw_data_dir, processed_data_dir)

    # Step 3 - load processed AIS files
    print("Loading processed AIS files...")
    processed_df = load_processed_csv_files(processed_data_dir)

    # Step 4 - visualization branch
    print("Extracting first arrivals...")
    first_arrivals_df = extract_first_arrivals_anywhere(processed_df)

    print("Creating vessel map...")
    create_first_arrivals_map(
        first_arrivals_df,
        output_path=output_html
    )

    # Step 5 - create weekly AIS features
    print("Creating weekly port activity features...")
    port_features_df = create_port_activity_features(
        processed_df,
        freq="W"
    )

    Path(batch_output_dir).mkdir(parents=True, exist_ok=True)

    port_features_df.to_csv(
        feature_output, 
        index=False
    )

    print(f"Saved AIS weekly port features to {feature_output}")
    print("AIS pipeline completed successfully!")


if __name__ == "__main__":
    main()

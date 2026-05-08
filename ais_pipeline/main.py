"""
Main entry point for this AIS data processing pipeline
"""
import sys

from downloader import download_ais_data
from processor import (
    process_all_zip_files,
    load_processed_csv_files,
    extract_first_arrivals_anywhere,
)
from plotting import create_first_arrivals_map


def main() -> None:
    """Run the AIS pipeline"""

    # Expect arguments from terminal
    if len(sys.argv) != 6:
        print(
            "Usage: python main.py <start_date> <end_date> <raw_data_dir> <output_html>"
        )
        sys.exit(1)

    start_date = sys.argv[1]
    end_date = sys.argv[2]
    raw_data_dir = sys.argv[3]
    processed_data_dir = sys.argv[4]
    output_html = sys.argv[5]

    print("Starting AIS pipeline...")

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

    # Step 4 - extract true first arrivals across all processed data
    print("Extracting first arrivals...")
    first_arrivals_df = extract_first_arrivals_anywhere(processed_df)

    # Step 5 - create map
    print("Creating vessel map...")
    create_first_arrivals_map(
        first_arrivals_df,
        output_path=output_html
    )

    print("Pipeline complete.")

if __name__ == "__main__":
    main()

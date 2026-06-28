"""
Main entry point for the financial data processing pipeline.
"""

import sys
from pathlib import Path

from financial_processor import (
    download_oil_data,
    create_weekly_oil_features,
    save_financial_features,
)

def main() -> None:
    """Run the financial data pipeline"""

    # Expect arguments from terminal
    if len(sys.argv) != 3:
        print(
            "Usage: python financial_main.py <start_date> <end_date>"
        )
        sys.exit(1)

    start_date = sys.argv[1]
    end_date = sys.argv[2]

    # Google Cloud Storage bucket paths for raw and processed data
    output_path = (
    "/Users/calebarrivillaga/Library/CloudStorage/"
    "GoogleDrive-calebar@umich.edu/My Drive/"
    "maritime-market-ml/cleaned_data/"
    "financial_weekly_features_master.csv"
    )

    print("Starting financial data pipeline...")

    oil_data = download_oil_data(
        start_date=start_date,
        end_date=end_date,
    )

    weekly_features = create_weekly_oil_features(oil_data)

    Path(output_path).parent.mkdir(
        parents=True, 
        exist_ok=True
    )

    save_financial_features(
        weekly_features, 
        output_path=output_path
    )

    print("Financial data pipeline completed successfully.")


if __name__ == "__main__":
    main()

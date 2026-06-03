"""
Functions for downloading AIS data files 
"""
from datetime import datetime, timedelta
from pathlib import Path
from urllib.error import ContentTooShortError, HTTPError, URLError
from urllib.request import urlretrieve
import time


def build_ais_url(date_str: str) -> str:
    """Build the NOAA AIS download URL for a single date."""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    year = date_obj.strftime("%Y")
    file_name = date_obj.strftime("AIS_%Y_%m_%d.zip")
    url = f"https://coast.noaa.gov/htdata/CMSP/AISDataHandler/{year}/{file_name}"
    return url

def build_file_name(date_str: str) -> str:
    """Build the AIS zip files name for single date."""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("AIS_%Y_%m_%d.zip")

def download_file_with_retries(
    url: str, 
    destination: Path, 
    retries: int = 3, 
    delay: int = 5
) -> bool: 
    """Download one file with retries and avoid keeping incomplete ZIP files."""

    temporary_destination = destination.with_suffix(".part")

    for attempt in range(1, retries + 1):
        try:
            if temporary_destination.exists():
                print(
                    f"Removing incomplete file from previous attempt: {temporary_destination}"
                )
                temporary_destination.unlink()  # Remove the incomplete file before retrying

            print(
                f"Downloading {destination.name}" 
                f" (Attempt {attempt}/{retries})..."
            )  

            urlretrieve(url, str(temporary_destination))

            temporary_destination.rename(destination)
            
            print(f"Saved to {destination}")

            return True
        
        except (
            HTTPError, 
            URLError, 
            ContentTooShortError
        ) as error:
            
            print(
                f"Attempt {attempt} failed "
                f"to download {destination.name}: {error}"
            )

            if temporary_destination.exists():
                print(f"Removing incomplete file: {temporary_destination}")
                temporary_destination.unlink()  # Remove the incomplete file after a failed attempt

            if attempt < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)

    print(f"Failed to download {destination.name} after {retries} attempts.")

    return False


def download_ais_data(start_date: str, end_date: str, save_dir: str) -> None:
    """Download AIS zip files for a date range."""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    output_path = Path(save_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    current = start

    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        file_name = build_file_name(date_str)
        url = build_ais_url(date_str)
        destination = output_path / file_name

        if destination.exists():
            print(f"File {file_name} already exists, skipping download.")
        else:
            download_file_with_retries(
                url, 
                destination=destination,
                retries=3,
                delay=5
            )

        current += timedelta(days=1)

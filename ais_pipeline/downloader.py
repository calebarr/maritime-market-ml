"""
Functions for downloading AIS data files 
"""
from datetime import datetime, timedelta
from pathlib import Path
from urllib.request import urlretrieve
import requests

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

        print(f"Downloading {file_name}...")

        try:
            urlretrieve(url, destination)
            print(f"Saved to {destination}")
        except requests.RequestException as error:
            print(f"Failed to download {file_name}: {error}")

        current += timedelta(days=1)

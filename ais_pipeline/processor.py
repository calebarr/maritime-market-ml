"""
Cleans data and processes AIS files
"""
from pathlib import Path
import zipfile
import pandas as pd
import numpy as np

def process_zip_in_chunks(zip_path: Path, chunksize: int = 100_000) -> pd.DataFrame:
    """Read one AIS zip file in chunks, clean each chunk, and return a reduced DataFrame."""

    cleaned_chunks = []

    with zipfile.ZipFile(zip_path, "r") as zf:
        csv_names = [name for name in zf.namelist() if name.endswith(".csv")]

        if not csv_names:
            return pd.DataFrame()

        with zf.open(csv_names[0]) as file:
            reader = pd.read_csv(file, chunksize=chunksize)

            for chunk in reader:
                cleaned_chunk = clean_ais_chunk(chunk)
                cleaned_chunks.append(cleaned_chunk)
    if  not cleaned_chunks:
        return pd.DataFrame()

    return pd.concat(cleaned_chunks, ignore_index=True)

def process_all_zip_files(raw_dir: str, processed_dir: str) -> None:
    """Process each raw AIS zip file and save a reduced CSV to the processed folder."""

    raw_path = Path(raw_dir)
    processed_path = Path(processed_dir)
    processed_path.mkdir(parents=True, exist_ok=True)

    zip_files = sorted(raw_path.glob("*.zip"))

    for zip_file in zip_files:
        print(f"Processing {zip_file.name}...")

        reduced_df = process_zip_in_chunks(zip_file)

        if reduced_df.empty:
            print(f"No usable data found in {zip_file.name}")
            continue

        output_name = f"{zip_file.stem}_processed.csv"
        output_file = processed_path / output_name

        reduced_df.to_csv(output_file, index=False)
        print(f"Saved processed file to {output_file}")

def load_processed_csv_files(processed_dir: str) -> pd.DataFrame:
    """Load all processed CSV files and combine them into one DataFrame."""

    processed_path = Path(processed_dir)
    csv_files = sorted(processed_path.glob("*_processed.csv"))

    df_list = []

    for csv_file in csv_files:
        print(f"Loading processed file {csv_file.name}...")
        df = pd.read_csv(csv_file)
        df["BaseDateTime"] = pd.to_datetime(df["BaseDateTime"], errors="coerce")
        df_list.append(df)

    if not df_list:
        raise ValueError("No processed CSV files were found.")

    return pd.concat(df_list, ignore_index=True)



def assign_port_names(df: pd.DataFrame, buffer: float = 1.3) -> pd.DataFrame:
    """Assign a port name based on vessel latitude and longitude."""

    port_regions = {
        "Los Angeles": (33.6, 33.9, -118.5, -118.0),
        "Long Beach": (33.7, 33.9, -118.25, -118.15),
        "Oakland": (37.7, 37.85, -122.35, -122.2),
        "Seattle": (47.5, 47.7, -122.4, -122.2),
        "New York": (40.6, 40.8, -74.1, -73.9),
        "Norfolk": (36.8, 37.1, -76.4, -76.2),
        "Savannah": (32.0, 32.2, -81.2, -80.8),
        "Charleston": (32.7, 32.9, -80.0, -79.8),
        "Miami": (25.75, 25.85, -80.2, -80.0),
        "Port Everglades": (26.05, 26.1, -80.15, -80.1),
        "Baltimore": (39.2, 39.3, -76.6, -76.5),
        "Philadelphia": (39.9, 40.0, -75.2, -75.1),
        "Houston": (29.6, 29.8, -95.2, -94.8),
        "New Orleans": (29.9, 30.1, -90.1, -89.9),
        "Jacksonville": (30.3, 30.5, -81.7, -81.3),
        "San Diego": (32.7, 32.8, -117.2, -117.1),
        "Boston": (42.3, 42.4, -71.1, -70.9),
        "Anchorage": (61.1, 61.3, -149.95, -149.8),
        "Honolulu": (21.3, 21.4, -157.9, -157.8),
        "Portland": (45.6, 45.7, -122.7, -122.6),
        "Puerto Rico": (18.2, 18.3, -66.3, -66.2),
        "Tacoma": (47.2, 47.4, -122.55, -122.35),
        "Port Arthur": (29.85, 29.95, -93.95, -93.85),
        "Beaumont": (30.0, 30.1, -94.15, -94.05),
        "Corpus Christi": (27.75, 27.9, -97.45, -97.25),
        "Baton Rouge": (30.4, 30.5, -91.25, -91.15),
        "Mobile": (30.6, 30.7, -88.1, -88.0),
        "Tampa": (27.9, 28.0, -82.5, -82.4),
        "San Francisco": (37.75, 37.85, -122.45, -122.3),
        "Wilmington (DE)": (39.7, 39.75, -75.55, -75.5),
        "Camden (NJ)": (39.9, 39.95, -75.1, -75.05),
        "Providence": (41.7, 41.8, -71.45, -71.35),

    }

    def get_port_name(lat: float, lon: float) -> str:
        for port, bounds in port_regions.items():
            min_lat, max_lat, min_lon, max_lon = bounds
            if (min_lat - buffer) <= lat <= (max_lat + buffer) and (
                min_lon - buffer
            ) <= lon <= (max_lon + buffer):
                return port
        return "Unknown"

    df = df.copy()
    df["Port Name"] = df.apply(lambda row: get_port_name(row["LAT"], row["LON"]), axis=1)
    return df

def clean_ais_chunk(df: pd.DataFrame) -> pd.DataFrame:
    """Clean AIS Data, keep relevant vessels, and return first arrivals by MMSI."""

    df = df.dropna(subset=["MMSI", "LAT", "LON", "BaseDateTime"]).copy()

    df["BaseDateTime"] = pd.to_datetime(df["BaseDateTime"], errors="coerce")
    df = df.dropna(subset=["BaseDateTime"])

    numeric_cols = [
        "SOG",
        "COG",
        "Heading",
        "Length",
        "Width",
        "Draft",
        "Cargo",
        "Status",
        "VesselType",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if "Heading" in df.columns:
        df["Heading"] = df["Heading"].replace(511, np.nan)

    df = df[df["LAT"].between(-90, 90) & df["LON"].between(-180, 180)]
    df = df[(df["LAT"] != 0) & (df["LON"] != 0)]

    for col in ["VesselName", "CallSign"]:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.upper()
                .replace({"NAN": np.nan})
            )

    good_types = list(range(70, 90)) + [30, 52]
    if "VesselType" in df.columns:
        df = df[df["VesselType"].isin(good_types)].copy()

    cols_to_drop = [
        "SOG",
        "COG",
        "Heading",
        "IMO",
        "VesselName",
        "Length",
        "Width",
        "TransceiverClass",
        "Cargo",
        "CallSign",
        "Draft",
    ]
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])

    return df

def extract_first_arrivals_anywhere(df : pd.DataFrame) -> pd.DataFrame:
    """Select the true first arrival per vessel and assign port names."""

    first_arrivals = (
        df.sort_values(["MMSI", "BaseDateTime"])
        .drop_duplicates("MMSI", keep="first")
        .copy()
    )

    return assign_port_names(first_arrivals)

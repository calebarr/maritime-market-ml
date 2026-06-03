"""
Generates the interactive map
"""

from pathlib import Path

import plotly.express as px
import pandas as pd

def create_first_arrivals_map(
    df: pd.DataFrame,
    output_path: str,
    sample_size = 5000
) -> None:
    """Create an interactive vessel map and save it as an HTML file."""

    plot_df = df.copy()

    if len(plot_df) > sample_size:
        plot_df = plot_df.sample(n=sample_size, random_state=42)

    # Remove unknown ports
    plot_df = plot_df[plot_df["Port Name"] != "Unknown"]

    fig = px.scatter_geo(
        plot_df,
        lat="LAT",
        lon="LON",
        color="Port Name",
        hover_data=["MMSI", "VesselType", "Port Name", "BaseDateTime"],
        title="First Arrivals: Vessel Locations by Port",
        projection="natural earth",
    )

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_file))

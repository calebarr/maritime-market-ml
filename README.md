Python >= 3.9 or newer recommended

# Maritime Market ML

Maritime Market ML is a machine learning project that investigates whether maritime shipping activity contains predictive signals for future oil market behavior.
The project combines Automatic Identification System (AIS) vessel tracking data with financial market data to explore the relationship between global shipping 
activity and future Brent crude oil returns. 

The project applies both supervised and unsupervised machine learning techniques to identify patterns in maritime activity and evaluate thier usefulness for 
understading and forcasting market behavior. 

# Data Sources

### Maritime Activity Data

- NOAA Automatic Identification System (AIS) vessel tracking data
- Vessel position, draft, speed, vessel type, and vessel dimensions
- Multiple U.S. ports from 2019 - 2024

# Financial Market Data

- Brent Crude Oil prices
- WTI Crude Oil prices
- Downloaded using yfinance

# Project Objectives

- Build a scalable AIS data processing pipeline
- Engineering maritime activity features from vessel tracking data
- Explore seasonal and operational shipping patterns
- Investigate whether maritime activity provides predictive information about future oil market returns
- Compare supervised and unsupervised machine learning approaches

# Machine Learning Methods

## Supervised Learning

- Linear Regression
- Decision Tree Regression
- Random Forest Regression
- Gradient Bossting Regression

Target Variable:
- Future 3-week Brent crude oil returns

## Unsupervised Learning
- K-Means Clustering
- Principal Component Analysis (PCA)

Objectives:
- Identify recuring maritime activity regimes
- Detect seasonal patterns in vessel traffic
- Explore latent structure within AIS derived features

# Feature Engineering

Weekly maritime activity features include:

- Tanker Vessel Count
- Cargo Vessel Count
- Unique Vessel Count
- Average Draft
- Average Speed Over Ground (SOG)
- Average Vessel Length

Financial features include:

- Brent Crude Oil Returns
- WTI Crude Oil Returns
- Future 3-Week Return targets

# Project Structure

```text
NOAA AIS Data
    |
    V
downloader.py
    |
    V
processor.py
    |
    V
combine_ais_batches.py
    |
    V
Weekly Maritime Feature Engineering
    |
Financial Market Data (yfinance)
    |
    V
Merged Maritime + Financial Dataset
    |
    V
Machine Learning Analysis
    |-- Supervised Learning
    |        |-- Linear Regression
    |        |-- Decision Tree
    |        |-- Random Forest
    |        |-- Gradient Boosting
    |
    |-- Unsupervised Learning
            |-- K-Mean Clustering
            |-- PCA
    |
    V
Results and Visualizations
```


# AIS Processing Pipeline 

1. Downlaod AIS vessel tracking data from NOAA
2. Filter and clean raw AIS vessel records
3. Process AIS files in batches to manage large datasets
4. Combine processed AIS batches into a unfied dataset
5. Aggregate vessel activity at the weekly level
6. Engineer maritime activity features
7. Merge maritime and financial datasets
8. Train and evaluate machine learning models
9. Analyze seasonal patterns and market relationships

## Requirements

Install dependencies with:

pip install -r requirements.txt

Required packages:

- pandas 
- numpy
- scikit-learn
- matplotlib
- seaborn
- plotly
- yfinance


# How to Run

Run the pipeline from the terminal:

'''bash
python main.py <start_date> <end_date> <raw_data_dir> <processed_dir> <output_html>

Example:
python main.py 2020-01-01 2020-01-10 data/raw data/processed outputs/first_arrivals_map.html



The pipeline performs the following steps:

1. Download AIS vessel tracking data
2. Loads and processes the AIS files
3. Extracts the first recorded arrival for each vessel
4. Generate an interactive map showing vessel positions



## Author 
Caleb Arrivillaga

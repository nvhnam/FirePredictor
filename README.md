# Cảnh báo sớm về các điểm cháy rừng ở Việt Nam

_(Forest Fire Early Warning System in Vietnam)_

**Institution:** University of Information Technology (UIT VNU-HCMC)  
**Course:** Data Mining and Applications – CS2207.CH203  
**Supervisor:** Dr. Võ Nguyễn Lê Duy

**Team member:**

- Nguyễn Ngọc Nam
- Nguyễn Việt Hoàng Nam
- Nguyễn Duy Ngọc
- Phạm Lê Thanh Nhàn

---

## Overview

This repository contains the source code and data pipeline for a Master's research project focused on predicting forest fire occurrences in Vietnam. Modeled as a binary classification problem, the system leverages historical satellite thermal anomalies and spatiotemporal environmental data to output early warning probabilities for high-risk zones.

<!--
## Data Architecture

The project utilizes a data-driven approach, extracting and fusing multi-source geospatial data via Google Earth Engine (GEE):

- **Target Labels:** Historical fire points from NASA FIRMS (MODIS/VIIRS), rigorously filtered using a custom _Fire Consistency Score_.
- **Meteorological Features:** Extracted from ERA5-Land, including event-time and 7-day antecedent metrics such as maximum temperature (`temp_max_7d`), dew point (`dew_evt`), surface pressure (`sp_evt`), accumulated rainfall (`rain_sum_7d`), wind components (`u10_evt`, `v10_evt`, `wind_evt`, `wind_max_7d`), and surface net solar radiation (`ssr_7d_mean`, `ssr_7d_sum`).
- **Vegetation & Topography:** MODIS NDVI (MOD13Q1) for vegetation stress, alongside SRTM DEM (30m) and ESA WorldCover (10m) for elevation, slope, aspect, and land cover classification.
- **Preprocessing:** The data pipeline automatically concatenates multi-batch GEE exports (e.g., merging 9 batch files into a final dataset of 81,321 records), handles missing coordinate data, and filters out null observations caused by cloud cover. -->

## Tech Stack

- **Data Pipeline:** Python (Pandas, Numpy), Google Earth Engine API.
- **Machine Learning:** Scikit-learn, XGBoost (Random Forest, Gradient Tree Boosting).
- **Web Deployment:** Streamlit, Folium (Interactive Mapping).

## Repository Structure

```text
├── app.py             # Streamlit frontend with Folium map integration
├── requirements.txt        # Python dependencies
└── README.md
```

## Quick Start

1. Clone the repository

   ```bash
   git clone https://github.com/nvhnam/FirePredictor.git
   cd FirePredictor
   ```

2. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit application

   ```bash
   streamlit run app.py
   ```

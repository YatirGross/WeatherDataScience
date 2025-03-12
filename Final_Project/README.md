# Efficient Representation of Location Features for Linear Predictive Models

## Overview
This project introduces a novel approach to encoding geographic locations using **3D Cartesian coordinates** instead of traditional categorical representations. By transforming latitude and longitude into (x, y, z) vectors, we improve predictive accuracy and computational efficiency for machine learning models.

## Key Features
- **3D Geospatial Encoding**: Converts latitude and longitude into 3D coordinates to preserve spatial relationships.
- **Geohash Comparison**: Evaluates the effectiveness of geohashing as a spatial encoding method.
- **Baseline Comparison**: Benchmarks performance against traditional encoding methods such as one-hot encoding and label encoding.



## Script: `location_to_db.py`
We provide an automated script to process and enhance location data:
- Retrieves latitude and longitude using **Geopy**.
- Converts geographic coordinates into **3D Cartesian format**.
- Updates a dataset with transformed location features.
- Ensures compatibility with machine learning models.

#### Required Python Packages
```bash
pip install pandas numpy geopy
```
### Usage
#### Basic:
```bash
python location_to_db.py path/to/data.csv --city_column City
```
#### With Address or/and Country:
```bash
python location_to_db.py path/to/data.csv --city_column City --address_col Address --country_col Country
```

## Results
- **Improved Model Performance**: 3D encoding outperformed traditional methods in global datasets like weather and cost of living but showed mixed results in other cases.
- **Efficient Representation**: The 3D approach significantly reduced dimensionality compared to one-hot encoding while maintaining spatial relationships.
- **Comparison to Baseline Approaches**: 3D encoding was evaluated against geohashing, one-hot encoding, and label encoding, showing improvements in some cases but not universally.
- **Dataset-Specific Effectiveness**: While beneficial for datasets where spatial continuity matters, traditional methods like one-hot encoding performed better for localized datasets (e.g., real estate and education data).




import argparse
import pandas as pd
import numpy as np
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

# geocoding function
def get_lat_lon(city_name, specific_address=None, country_name=None, cache={}, max_retries=3, sleep_time=2):
    query_parts = [city_name]
    if specific_address:
        query_parts.insert(0, specific_address)
    if country_name:
        query_parts.append(country_name)
    query = ", ".join(query_parts)

    if query in cache:
        return cache[query]

    geolocator = Nominatim(user_agent="geo_pipeline", timeout=10)

    for attempt in range(max_retries):
        try:
            location = geolocator.geocode(query, timeout=10)
            if location:
                cache[query] = (location.latitude, location.longitude)
                return cache[query]
            else:
                cache[query] = None
                return None
        except (GeocoderTimedOut, GeocoderServiceError):
            print(f"Warning: Geocoding timeout for '{query}'. Retrying ({attempt + 1}/{max_retries})...")
            time.sleep(sleep_time)

    print(f"Error: Failed to fetch coordinates for '{query}' after {max_retries} retries.")
    return None

# conversion function
def latlon_to_3d(lat, lon):
    lat, lon = np.radians(lat), np.radians(lon)
    R = 6371  # Earth's radius in km

    x = R * np.cos(lat) * np.cos(lon)
    y = R * np.cos(lat) * np.sin(lon)
    z = R * np.sin(lat)

    return np.array([x, y, z])

# Main processing function supporting optional columns and inplace CSV update
def process_csv_inplace(csv_path, city_col, address_col=None, country_col=None):
    df = pd.read_csv(csv_path)

    latitudes = []
    longitudes = []
    coords_3d_x = []
    coords_3d_y = []
    coords_3d_z = []

    cache = {}

    total_rows = len(df)

    for idx, row in df.iterrows():
        city_name = row[city_col]
        specific_address = row[address_col] if address_col and pd.notna(row[address_col]) else None
        country_name = row[country_col] if country_col and pd.notna(row[country_col]) else None

        print(f"Processing row {idx+1}/{total_rows}: city='{city_name}', address='{specific_address}', country='{country_name}'")

        result = get_lat_lon(city_name=city_name,
                             specific_address=specific_address,
                             country_name=country_name,
                             cache=cache)

        if result is not None:
            lat, lon = result
            coord_3d = latlon_to_3d(lat, lon)
            latitudes.append(lat)
            longitudes.append(lon)
            coords_3d_x.append(coord_3d[0])
            coords_3d_y.append(coord_3d[1])
            coords_3d_z.append(coord_3d[2])
        else:
            latitudes.append(None)
            longitudes.append(None)
            coords_3d_x.append(None)
            coords_3d_y.append(None)
            coords_3d_z.append(None)

    # Add new columns directly to DataFrame
    df["latitude"] = latitudes
    df["longitude"] = longitudes
    df["coord_x"] = coords_3d_x
    df["coord_y"] = coords_3d_y
    df["coord_z"] = coords_3d_z

    # Save updated DataFrame back to CSV inplace
    df.to_csv(csv_path, index=False)
    
    print(f"✅ Updated CSV saved inplace at '{csv_path}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add 3D coordinates directly into CSV file.")
    
    parser.add_argument("csv_path", help="Path to the input CSV file.")
    
    parser.add_argument("--city_col", required=True,
                        help="Name of the column containing city names.")
    
    parser.add_argument("--address_col", default=None,
                        help="(Optional) Name of the column containing specific addresses.")
    
    parser.add_argument("--country_col", default=None,
                        help="(Optional) Name of the column containing country names.")

    args = parser.parse_args()

    process_csv_inplace(csv_path=args.csv_path,
                        city_col=args.city_col,
                        address_col=args.address_col,
                        country_col=args.country_col)
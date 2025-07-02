# downloader/download_climate.py

import requests
import pandas as pd
import os
import io

# Chilika Lagoon location
lat, lon = 19.72, 85.3
start_year, end_year = 2015, 2024

# NASA POWER API
url = "https://power.larc.nasa.gov/api/temporal/monthly/point"
params = {
    "parameters": "T2M_MAX,PRECTOTCORR,ALLSKY_SFC_SW_DWN",
    "community": "AG",
    "latitude": lat,
    "longitude": lon,
    "start": start_year,
    "end": end_year,
    "format": "CSV"
}

print(f"🌍 Fetching climate data from NASA for Chilika ({lat}, {lon})...")
resp = requests.get(url, params=params)
resp.raise_for_status()

# Parse the response
raw = resp.text
csv_data = raw.split("-END HEADER-")[1].strip()
df = pd.read_csv(io.StringIO(csv_data), header=None)

# Reshape NASA format
def reshape_param(df, param_name):
    df_p = df[df[0] == param_name].copy()
    df_p.columns = ["PARAM", "YEAR", "JAN", "FEB", "MAR", "APR", "MAY", "JUN",
                    "JUL", "AUG", "SEP", "OCT", "NOV", "DEC", "ANN"]
    df_p = df_p.drop(columns=["PARAM", "ANN"])
    df_p = df_p.melt(id_vars="YEAR", var_name="Month", value_name=param_name)
    return df_p

df_temp = reshape_param(df, "T2M_MAX")
df_rain = reshape_param(df, "PRECTOTCORR")
df_sun = reshape_param(df, "ALLSKY_SFC_SW_DWN")

# Merge and clean
merged = df_temp.merge(df_rain, on=["YEAR", "Month"]).merge(df_sun, on=["YEAR", "Month"])
merged["Month_Name"] = merged["Month"]
merged["Month"] = merged["YEAR"].astype(str) + "-" + merged["Month"]
merged = merged.rename(columns={
    "T2M_MAX": "TempMax_C",
    "PRECTOTCORR": "Rain_mm",
    "ALLSKY_SFC_SW_DWN": "Sunlight_h"
})
merged = merged[["Month", "Month_Name", "TempMax_C", "Rain_mm", "Sunlight_h"]]

# Save
data_dir = os.path.join(os.path.dirname(__file__), "../data")
os.makedirs(data_dir, exist_ok=True)
outpath = os.path.join(data_dir, "odisha_climate.csv")
merged.to_csv(outpath, index=False)

print(f"✅ Saved to {outpath}")

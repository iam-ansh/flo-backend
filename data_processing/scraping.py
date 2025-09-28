from ftplib import FTP
import netCDF4 as nc
import numpy as np
import pandas as pd
import xarray as xr
import requests
from bs4 import BeautifulSoup
import io
from datetime import datetime
import json
import math
from pathlib import Path

# # OSError: [Errno 113] No route to host  ---------------------->   your network is low


def dictToJSON(dict1, filename):
    with open(f'{filename}.json', 'a') as f:
        json.dump(dict1, f, indent=4)
        f.write(",")
        f.close()
    # print("done into json ...")


def extraction(ds, filename):
    json_dir = Path("jsons")
    csv_dir = Path("csvs")
    json_dir.mkdir(parents=True, exist_ok=True)
    csv_dir.mkdir(parents=True, exist_ok=True)

    skip_vars = {
        "PRES_QC", "TEMP_QC", "PSAL_QC", "PRES_ADJUSTED", "TEMP_ADJUSTED", "PSAL_ADJUSTED",
        "PRES_ADJUSTED_QC", "TEMP_ADJUSTED_QC", "PSAL_ADJUSTED_QC", "PRES_ADJUSTED_ERROR",
        "TEMP_ADJUSTED_ERROR", "PSAL_ADJUSTED_ERROR", "STATION_PARAMETERS", "DIRECTION",
        "DATA_CENTER", "DATA_MODE", "FLOAT_SERIAL_NO", "POSITION_QC", "PROFILE_PRES_QC",
        "PROFILE_TEMP_QC", "PROFILE_PSAL_QC", "CONFIG_MISSION_NUMBER"
    }

    dict1 = {}
    n = 0

    for var in ds.variables:
        if len(ds[var].shape) == 1:     # means put in json
            dict1[var] = ds[var].values
            n = len(ds[var])

        if var in skip_vars: continue
        # if len(ds[var].shape)>0:
        #     if len(ds[var].shape) == 3: continue
        #     for i in range(ds[var].shape[0]):
        #         print(value.values)
        # if var == "PRES":
        #     # print(ds[var].isel(N_PROF=0).values)
        #     for i in range(ds[var].shape[0]):
        #         print(ds[var].isel(N_LEVELS=i).values)
        # elif var == "TEMP":
        #     # print(ds[var].isel(N_PROF=0).values)
        #     for i in range(ds[var].shape[0]):
        #         print(value.values)
        # elif var == "PSAL":
        #     # print(ds[var].isel(N_PROF=0).values)
        #     for i in range(ds[var].shape[0]):
        #         print(value.values)
        # print(ds[var].__init__)
        # print(var.long_name)
        # print(var._FillValue)
    
    # print(dict1)

    rows = []
    json_data = {}

    for i in range(n):
        dict_form = {}
        for k, v in dict1.items():
            value = v[i]
            if isinstance(value, bytes):
                value = value.decode("utf-8").strip()
            if isinstance(value, np.float64):
                value = float(value)
            if isinstance(value, np.datetime64):
                value = str(value)
            if isinstance(value, float) and math.isnan(value):
                value = "-"
            dict_form[k] = value
        rows.append(dict_form)

        
        key = f'{dict_form["PLATFORM_NUMBER"]}/{dict_form["JULD"]}'
        json_data[key] = dict_form

   
    json_path = json_dir / f"{filename}.json"
    json_path.write_text(json.dumps(json_data, indent=4), encoding="utf-8")


    csv_path = csv_dir / f"{filename}.csv"
    pd.DataFrame(rows).to_csv(csv_path, index=False)

    print(f"JSON saved to {json_path}")
    print(f"CSV saved to {csv_path}")


def fun(link):
    print(f"requesting for file {link}...")
    response = requests.get(f"https://data-argo.ifremer.fr/geo/indian_ocean/2025/09/{link}", stream=True)
    data = response.content
    # print(data)
    print("converting into bytes ...")
    bytesData = io.BytesIO(data)
    # print(bytesData)
    print("opening in dataset ...")
    ds = xr.open_dataset(bytesData)
    # print(ds)
    extraction(ds, link[:len(link)-3])


url = "https://data-argo.ifremer.fr/geo/indian_ocean/2025/09/"
print("requesting on url ...")
r = requests.get(url)
text = r.text
# print(text)
print("parsing html ...")
soup = BeautifulSoup(text, 'html.parser')
print("links are :-")
for link in soup.find_all('a'):
    if(link.get('href').__contains__("nc")) :
        print(link.get('href'))
        fun(link.get('href'))
        # break




    # DATA_TYPE = bytearray()
    # FORMAT_VERSION = bytearray()
    # HANDBOOK_VERSION = bytearray()
    # REFERENCE_DATE_TIME = bytearray()
    # DATE_CREATION = bytearray()
    # DATE_UPDATE = bytearray()
    # PLATFORM_NUMBER = [bytearray()]
    # PROJECT_NAME = [bytearray()]
    # PI_NAME = [bytearray()]
    # STATION_PARAMETERS = [[bytearray()]]
    # CYCLE_NUMBER = []
    # DIRECTION = bytearray()
    # DATA_CENTRE = [bytearray()]
    # DC_REFERENCE = [bytearray()]
    # DATA_STATE_INDICATOR = [bytearray()]
    # DATA_MODE = bytearray()
    # PLATFORM_TYPE = [bytearray()]
    # FLOAT_SERIAL_NO = [bytearray()]
    # FIRMWARE_VERSION = [bytearray()]
    # WMO_INST_TYPE = [bytearray()]
    # JULD = []
    # JULD_QC = bytearray()
    # JULD_LOCATION = []
    # LATITUDE = []
    # LONGITUDE = []
    # POSITION_QC = bytearray()
    # POSITIONING_SYSTEM = [bytearray()]
    # PROFILE_PRES_QC = bytearray()
    # PROFILE_TEMP_QC = bytearray()
    # PROFILE_PSAL_QC = bytearray()
    # VERTICAL_SAMPLING_SCHEME = [bytearray()]
    # CONFIG_MISSION_NUMBER = []
    # PRES = [[]]
    # PRES_QC = [bytearray()]
    # PRES_ADJUSTED = [[]]
    # PRES_ADJUSTED_QC = [bytearray()]
    # PRES_ADJUSTED_ERROR = [[]]
    # TEMP = [[]]
    # TEMP_QC = [bytearray()]
    # TEMP_ADJUSTED = [[]]
    # TEMP_ADJUSTED_QC = [bytearray()]
    # TEMP_ADJUSTED_ERROR = [[]]
    # PSAL = [[]]
    # PSAL_QC = [bytearray()]
    # PSAL_ADJUSTED = [[]]
    # PSAL_ADJUSTED_QC = [bytearray()]
    # PSAL_ADJUSTED_ERROR = [[]]
    # PARAMETER = [[[bytearray()]]]
    # SCIENTIFIC_CALIB_EQUATION = [[[bytearray()]]]
    # SCIENTIFIC_CALIB_COEFFICIENT = [[[bytearray()]]]
    # SCIENTIFIC_CALIB_COMMENT = [[[bytearray()]]]
    # SCIENTIFIC_CALIB_DATE = [[[bytearray()]]]
    # HISTORY_INSTITUTION = []
    # HISTORY_STEP = []
    # HISTORY_SOFTWARE = []
    # HISTORY_SOFTWARE_RELEASE = []
    # HISTORY_REFERENCE = []
    # HISTORY_DATE = []
    # HISTORY_ACTION = []
    # HISTORY_PARAMETER = []
    # HISTORY_START_PRES = []
    # HISTORY_STOP_PRES = []
    # HISTORY_PREVIOUS_VALUE = []
    # HISTORY_QCTEST = []

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

# # OSError: [Errno 113] No route to host  ---------------------->   your network is low


def dictToJSON(dict1, filename):
    with open(f'{filename}.json', 'a') as f:
        json.dump(dict1, f, indent=4)
        f.write(",")
        f.close()
    # print("done into json ...")


def extraction(ds, filename):
    
    dict1 = {}
    n = 0

    for var in ds.variables:
        
        if len(ds[var].shape) == 1: # means put in json
            # print(var)
            dict1[var] = ds[var].values
            n = len(ds[var])
        

        if var == "PRES_QC" or var == "TEMP_QC" or var == "PSAL_QC" or var == "PRES_ADJUSTED" or var == "TEMP_ADJUSTED" or var == "PSAL_ADJUSTED" or var == "PRES_ADJUSTED_QC" or var == "TEMP_ADJUSTED_QC" or var == "PSAL_ADJUSTED_QC" or var == "PRES_ADJUSTED_ERROR" or var == "TEMP_ADJUSTED_ERROR" or var == "PSAL_ADJUSTED_ERROR" or var == "STATION_PARAMETERS" or var == "DIRECTION" or var == "DATA_CENTER" or var == "DATA_MODE" or var == "FLOAT_SERIAL_NO" or var == "POSITION_QC" or var == "PROFILE_PRES_QC" or var == "PROFILE_TEMP_QC" or var == "PROFILE_PSAL_QC" or var == "CONFIG_MISSION_NUMBER": continue
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

    with open(f'{filename}.json', 'a') as f:
            f.write("{")
            f.close()

    for i in range(n):
        dict_form = {}
        for k,v in dict1.items():
            value = v[i]
            if isinstance(value, bytes):  
                value = value.decode("utf-8").strip()
            if isinstance(value,  np.float64):
                # print("float64")
                value = float(value)
            if isinstance(value,  np.datetime64):
                value = str(value)
            if isinstance(value, float) and math.isnan(value):
                value = "-"
            # print(type(value))
            dict_form[k] = value
        # print(dict_form)

        with open(f'{filename}.json', 'a') as f:
            f.write(f'"{dict_form["PLATFORM_NUMBER"]}/{dict_form["JULD"]}":')
            f.close()

        dictToJSON(dict_form, filename)


    with open(f'{filename}.json', "r") as file:
        content = file.read()
        if content:
            content = content[:-1]

        with open(f'{filename}.json', "w") as f:
            f.write(content)
            f.close()
    
        file.close()

    with open(f'{filename}.json', 'a') as f:
        f.write("}")
        f.close()
    
    print("json convertion done ...")


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

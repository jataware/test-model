import click
import random
import json
import time
import pandas as pd
from faker import Faker
from datetime import datetime
from collections import OrderedDict
import urllib.request
import os
import requests
from netCDF4 import Dataset, date2num
import numpy as np
import openpyxl
import xarray as xr
import rasterio
from rasterio.transform import from_origin
from openpyxl import Workbook
from scipy.interpolate import griddata
import shutil

if not os.path.exists('output'):
    os.mkdir('output')

if not os.path.exists('media'):
    os.mkdir('media')    

@click.command()
@click.option('--temp', type=float, required=True, help='Percentage perturbation to temperature.')
def main(temp):
    params = open('configFiles/parameters.json').read()
    params = json.loads(params)

    configFileData = open('configFiles/categories.json').read()
    configFileData = json.loads(configFileData)


    print('Beginning to download file from S3...')

    df = pd.read_csv('input/input_csv.csv')
    df['scenario'] = df['OMEGA'].apply(lambda x: random.choice(['high','medium','low']))
    df['T'] = df['T'] * temp
    df.to_csv('output/output_csv.csv', index=False)

    shutil.copy('input/input_excel.xlsx', 'output/output_excel.xlsx')
    shutil.copy('input/input_netcdf.nc', 'output/input_netcdf.nc')
    shutil.copy('input/input_geotiff_feature_bands.tif', 'output/output_geotiff_feature_bands.tif')
    shutil.copy('input/input_geotiff_time_bands.tif', 'output/output_geotiff_time_bands.tif')

def get_media():
    image_urls = ['https://i.kym-cdn.com/entries/icons/facebook/000/000/774/lime-cat.jpg',
                  'https://pbs.twimg.com/profile_images/1356088845821857795/1WWMDwIQ_400x400.jpg']
    for url in image_urls:
        filename = url.split('/')[-1]
        img_data = requests.get(url).content
        with open(f'media/{filename}', 'wb') as handler:
            handler.write(img_data)
        print(f"Wrote media: {filename}")
    return


if __name__ == "__main__":
    get_media()
    main()
    print("SUCCESS")

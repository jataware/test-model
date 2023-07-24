import click
import random
import json
import time
import pandas as pd
from faker import Faker
from collections import OrderedDict
import urllib.request
import os
import requests
from netCDF4 import Dataset
import numpy as np
import openpyxl
import xarray as xr
import rasterio
from rasterio.transform import from_origin
from openpyxl import Workbook
from scipy.interpolate import griddata
if not os.path.exists('output'):
    os.mkdir('output')

if not os.path.exists('media'):
    os.mkdir('media')    

@click.command()
@click.option('--temp', type=float, required=True, help='Percentage perturbation to temperature.')
def main(temp):
    params = open('configFiles/parameters.json').read()
    params = json.loads(params)

    configFileData = open('configFiles/fakeDataType.json').read()
    configFileData = json.loads(configFileData)


    print('Beginning to download file from S3...')

    url = 'https://jataware-world-modelers.s3.amazonaws.com/dummy-model/input.csv'
    urllib.request.urlretrieve(url, 'input.csv')


    locales = OrderedDict([
        ('en-US', 1)
    ])
    fake = Faker(locales)
    f = fake['en_US']    
    data = []

    perturbation = 1 + (params['rainfall']*temp)
    getColorHue = configFileData['color_hue']
    for i in range(100):
        obj = dict(latitude=f.latitude(),
                   longitude=f.longitude(),
                   date=f.date(),
                   var_1=random.random()*perturbation,
                   var_2=f.color(hue=getColorHue))
        data.append(obj)

    df = pd.DataFrame(data)
    print(df.head())
    fname = f"output_{params['rainfall']}_{temp}"
    df.to_csv(f'output/{fname}.csv', index=False)
    print(f"Saved output as /model/output/{fname}.csv")

    # Save as Excel
    df.to_excel(f'output/{fname}.xlsx', index=False)
    print(f"Saved output as /model/output/{fname}.xlsx")

    # Save as GeoTIFF
    # Restricting to 'latitude', 'longitude' and 'value' as it's mandatory for geospatial data
    df_geo = df[['latitude', 'longitude', 'var_1']]
    df_geo['latitude'] = df_geo['latitude'].astype(float)
    df_geo['longitude'] = df_geo['longitude'].astype(float)    

    # Define the grid size
    grid_size_lat = 100
    grid_size_lon = 100

    # Create the grid
    lon_grid = np.linspace(df_geo['longitude'].min(), df_geo['longitude'].max(), grid_size_lon)
    lat_grid = np.linspace(df_geo['latitude'].min(), df_geo['latitude'].max(), grid_size_lat)
    lon_grid, lat_grid = np.meshgrid(lon_grid, lat_grid)

    # Interpolate the values
    values_grid = griddata(df_geo[['longitude', 'latitude']].values, df_geo['var_1'].values, (lon_grid, lat_grid), method='linear')

    transform = from_origin(df_geo['longitude'].min(), df_geo['latitude'].max(), (df_geo['longitude'].max()-df_geo['longitude'].min())/grid_size_lon, (df_geo['latitude'].max()-df_geo['latitude'].min())/grid_size_lat)
    with rasterio.open(f'output/{fname}.tif', 'w', driver='GTiff', height=grid_size_lon, width=grid_size_lat, count=1, dtype=str(values_grid.dtype), crs='+proj=latlong', transform=transform) as dst:
        dst.write(values_grid, 1)
    print(f"Saved output as /model/output/{fname}.tif")

    # Create an xarray Dataset from the gridded data
    ds = xr.Dataset(
        {'var_1': (('latitude', 'longitude'), values_grid)},
        coords={'longitude': (('longitude',), lon_grid[0, :]),
                'latitude': (('latitude',), lat_grid[:, 0])})

    # Save the xarray Dataset to a netCDF file
    ds.to_netcdf(f'output/{fname}.nc')
    print(f"Saved output as /model/output/{fname}.nc")

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

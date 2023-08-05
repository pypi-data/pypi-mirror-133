'''
reinan br <slimchatuba@gmail.com>
31/12/2021 15:46
Lib: noawclg (light version from noaawc) v0.0.1b0
=================================================================
Why it work use the GPLv3 LICENSE?
-----------------------------------------------------------------
    this project use the license gplv3  because i have a hate 
    that the other privates projects in the bussines that use
    the 'open data' from noaa in the your closed source,
    and i see it, i getted the iniciative that make the ant way
    from this method, and making the condiction that who use it
    project on your personal project, open your project, or win
    a process.

=================================================================
waht is for it project?
-----------------------------------------------------------------
    This project is for a best development in works with 
    climate prediction and getting it data from the 
    opendata in noaa site on type netcdf.

=================================================================
it's a base from the noaawc lib
-----------------------------------------------------------------
    This will are the base from a lib very more big from it's,
    your name will call as 'nooawc', and because from need
    mpl_toolkits.basemap, your work will are possible only
    the anaconda.
'''

# importing the need lib's
#import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from datetime import datetime
# import requests as rq
# from bs4 import beautifulsoup as soup

date_now = datetime.now
date_base_param = date_now().strftime('%Y/%m/%d')

# function for get data from noaa dataOpen 
# Tḧis function is the base from the all work
# beacause its getting the data from noaa
def get_noaa_data(date:str=date_base_param,hour:str='00'):
    '''
        params:
            date: str
                input a date in inverse mode
    '''
    date_input=date
    date=date.split('/')
    date=''.join(date)
    #print(date)
    # url base from the data noaa in GFS 0.25
    url_cdf=f'https://nomads.ncep.noaa.gov/dods/gfs_0p25/gfs{date}/gfs_0p25_{hour}z'
    
    # reading the data required in the param's
    file = xr.open_dataset(url_cdf)
    data = file.variables
    #data_about=file.variables['long_name']
    #print(data_key,"->",data.attrs['long_name'],f'[{date_input}]')
    
    return data

    
    
# getting the list data present in the data noaa GFS 0.25
def get_noaa_keys(date=date_base_param,hour='00'):
    '''
    '''
    date_input=date
    date=date.split('/')
    date=''.join(date)
    
    url_cdf=f'https://nomads.ncep.noaa.gov/dods/gfs_0p25/gfs{date}/gfs_0p25_{hour}z'
    
    file = xr.open_dataset(url_cdf)
    keys = file.variables.keys()
    keys_about = []
    for key in keys:
        about_key = file.variables[key].attrs['long_name'] 
        keys_about.append({key:about_key})
    
    return np.array(keys_about)




'''
lon_j = 360-40.5
dt_jua=file.sel(lon=lon_j,lat=-9.41,method='nearest')
dt_jua['tmpsfc']=dt_jua['tmpsfc']-273
'''

# getting data only a just point
# this project in question needed
# from a great logic work on the 
# changing lon.

def get_data_from_point(point,date=date_base_param,hour='00',data_key='tmpsfc'):
    '''
    '''
    date_input=date
    date=date.split('/')
    date=''.join(date)
    url_cdf=f'https://nomads.ncep.noaa.gov/dods/gfs_0p25/gfs{date}/gfs_0p25_{hour}z'
    file = xr.open_dataset(url_cdf)
    data = file.variables
    
    lat,lon = point[0],abs(point[1]) if point[1]<0 else 360-point[1]
    print(f'lat: {lat}, lon: {lon}')
    data_point = file.sel(lon=lon,lat=lat,method='nearest')
    data_point = {'time':data_point.variables['time'],'data':data_point.variables[data_key]}
    
    return data_point
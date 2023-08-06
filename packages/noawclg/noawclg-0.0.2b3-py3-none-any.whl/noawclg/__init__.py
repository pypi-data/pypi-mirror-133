from .main import get_noaa_data

import json

with open('config.json','r') as conf:
    config = json.loads(conf.read())

__version__ = config['version']
__author__ = config['author']



all = [get_noaa_data,__version__,__author__]
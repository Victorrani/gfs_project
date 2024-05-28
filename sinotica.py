#python3.8.3

import sys
import pygrib
import matplotlib 
import matplotlib.pyplot as plt
import cartopy, cartopy.crs as ccrs   
import cartopy.io.shapereader as shpreader
import cartopy.feature as cfeature  
import numpy as np
import scipy.ndimage as ndimage
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import matplotlib.lines as mlines
import pandas as pd
from metpy.calc import reduce_point_density
from metpy.io import metar
from metpy.plots import current_weather, sky_cover, StationPlot
import metpy.plots as mpplots
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
import xarray as xr


print('Novo mapa de sinótica')
print('')
DIRGFS='/home/victor/Desktop/master_python/DADOS/gfs.2023112100.1p00.f000'
DIROUT='/home/victor/Desktop/master_python/DADOS/'
print('')
print(DIRGFS)
print('')

ds = xr.open_dataset(DIRGFS, engine='cfgrib', filter_by_keys={'typeOfLevel': 'surface'})


fig = plt.figure(figsize=(10,10))

regiao = [-120, 0, -60, 15]

##Criação do mapa com o projeção
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.set_extent(regiao, crs=ccrs.PlateCarree())

##Funcionalidades do mapa
ax.add_feature(cfeature.LAND, color='lightgray')
ax.add_feature(cfeature.COASTLINE, edgecolor='black')
ax.add_feature(cfeature.OCEAN, color='lightblue')
ax.add_feature(cfeature.BORDERS)

ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

figout=DIROUT+'teste.jpeg'
plt.savefig(str(figout),bbox_inches='tight', pad_inches=0.1, dpi=300, transparent=False)

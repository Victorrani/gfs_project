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


def latlon(lista):


  regiao = lista
  x_min, x_max = regiao[0], regiao[1]
  y_min, y_max = regiao[2], regiao[3]
##Define de onde até onde a marcação vai com passos definidos
  x_ticks = np.arange(x_min, x_max + 1, 20)
  y_ticks = np.arange(y_min, y_max + 1, 10)
##condição
  y_ticklabels = [f'{abs(tick)}° S' if tick < 0 else f'{tick}° N' if tick > 0 else '0' for tick in y_ticks]
  x_ticklabels = [f'{abs(tick)}° W' if tick < 0 else f'{tick}° E' if tick > 0 else '0' for tick in x_ticks]

  ax.set_xticks(x_ticks)
  ax.set_yticks(y_ticks)

  ax.set_xticklabels(x_ticklabels)
  ax.set_yticklabels(y_ticklabels)



####################################################################################################
try:
    data=str(sys.argv[1])
except:
    print ("Faltou passar a data e hora Ex: 2022010300")
    quit()

dirfigs="/home/victor/Desktop/master_python/FIGURAS"   


arquivo_teste='/home/victor/Desktop/master_python/DADOS/gfs025.202304200000_000.grb2'



##########################################################################

#open GFS file
gfs = pygrib.open(arquivo_teste)
print(gfs)

colors = [(1, 1, 1), (0, 0, 1), (1, 0, 0), (1, 1, 1)]
cmap_name = 'custom_blue_red'
cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=256)

titulo = 'MSLP (black, hPa), 1000 - 500 thickness (red/blue, dam), 250 hPa wind speedy (shaded, m/s)\nGFS 0.25 2023/04/02 00Z'

regiao = [-120, 0, -60, 15]

##variáveis

select_u250 = gfs.select(name='U component of wind', typeOfLevel='isobaricInhPa', level=250)[0]
select_v250 = gfs.select(name='V component of wind', typeOfLevel='isobaricInhPa', level=250)[0]

u250, lats, lons = select_u250.data(lat1=regiao[2],lat2=regiao[3],lon1=regiao[0]+360,lon2=regiao[1]+360)
v250, lats, lons = select_v250.data(lat1=regiao[2],lat2=regiao[3],lon1=regiao[0]+360,lon2=regiao[1]+360)

select_pmsl=gfs.select(name='Pressure reduced to MSL')[0]
pmsl, lats, lons = select_pmsl.data(lat1=regiao[2],lat2=regiao[3],lon1=regiao[0]+360,lon2=regiao[1]+360)

#select_geo500=gfs.select()[348]

                       
select_geo500=gfs.select(name='Geopotential Height', typeOfLevel='isobaricInhPa', level=500)[0]
geo500, lats, lons = select_geo500.data(lat1=regiao[2],lat2=regiao[3],lon1=regiao[0]+360,lon2=regiao[1]+360)
select_geo1000=gfs.select()[557]
geo1000, lats, lons = select_geo1000.data(lat1=regiao[2],lat2=regiao[3],lon1=regiao[0]+360,lon2=regiao[1]+360)

deltageo = (geo500 - geo1000) / 10
pmsl = pmsl / 100
mag250 = np.sqrt((u250*u250)+(v250*v250))

pmsl = ndimage.gaussian_filter(pmsl, sigma=5, order=0)
mag250 = ndimage.gaussian_filter(mag250, sigma=5, order=0)
deltageo = ndimage.gaussian_filter(deltageo, sigma=5, order=0)


fig = plt.figure(figsize=(10,10))

##Criação do mapa com o projeção
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.set_extent(regiao, crs=ccrs.PlateCarree())

##Funcionalidades do mapa
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS)

shapefile = list(shpreader.Reader('/home/victor/Desktop/master_python/PYTHON/shapefiles/BR_UF_2019.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black',facecolor='none', linewidth=0.3, zorder=300)

##Jatos de altos níveis
data_min = 35
data_max = 100
interval = 5
levels = np.arange(data_min,data_max,interval)


img1 = ax.contourf(lons, lats, mag250,cmap=cm, levels=levels,vmin=35,  transform=ccrs.PlateCarree(), zorder=300, alpha=0.75)
img2 = ax.contour(lons, lats, mag250, colors='white', linewidths=0.2, levels=levels, transform=ccrs.PlateCarree(), zorder=301)
plt.colorbar(img1, label='Isotacas (m/s)', orientation='horizontal', pad=0.05, fraction=0.05)

##pmsl
data_min_pmsl = 840
data_max_pmsl = 1200
interval_pmsl = 4
levels_pmsl = np.arange(data_min_pmsl, data_max_pmsl,interval_pmsl)


img3 = ax.contour(lons, lats, pmsl, colors='black', linewidths=0.7, levels=levels_pmsl, zorder=305)
ax.clabel(img3, inline=1, inline_spacing=0, fontsize='10',fmt = '%1.0f', colors= 'black')
latlon(regiao)

##espessura da camada <540dam
data_min_espessura = 0
data_max_espessura = 540
interval_espessura = 6
levels = np.arange(data_min_espessura ,data_max_espessura ,interval_espessura)


img4 = ax.contour(lons, lats, deltageo, colors='blue', linestyles='dashed', linewidths=1, levels=levels, zorder=306)
ax.clabel(img4, inline=1, inline_spacing=0, fontsize='10',fmt = '%1.0f', colors= 'blue')

##espessura da camada >540dam
data_min_espessura2 = 540
data_max_espessura2 = 1000
interval_espessura2 = 6
levels = np.arange(data_min_espessura2,data_max_espessura2,interval_espessura2)


img5 = ax.contour(lons, lats, deltageo, colors='red', linestyles='dashed', linewidths=1, levels=levels, zorder=307)
ax.clabel(img5, inline=1, inline_spacing=0, fontsize='10',fmt = '%1.0f', colors='red')

ax.grid()

plt.title(titulo, loc='left')

		
        ##save image
        
figout=dirfigs+'/'+'_gfs025_sinotica_250hpa_'+data+'00.teste.jpeg'
plt.savefig(str(figout),bbox_inches='tight', pad_inches=0.1, dpi=300, transparent=False)

exit  

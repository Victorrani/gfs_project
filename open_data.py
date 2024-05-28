import xarray as xr
import cfgrib


arquivo2 = "/home/victor/Desktop/master_python/PYTHON/DADOS/gfs.t00z.pgrb2.0p25.f000"
ds2 = xr.open_mfdataset(arquivo2, engine="cfgrib", filter_by_keys={'typeOfLevel': 'isobaricInhPa'})
print(ds2)


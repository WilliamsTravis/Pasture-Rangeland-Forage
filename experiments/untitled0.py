# -*- coding: utf-8 -*-
"""

Just a rain map

Created on Sat Apr 28 12:07:10 2018

@author: trwi0358
"""

runfile('C:/Users/trwi0358/Github/Pasture-Rangeland-Forage/functions_git.py', wdir='C:/Users/trwi0358/Github/Pasture-Rangeland-Forage')
import warnings
warnings.filterwarnings("ignore") #This is temporary, toggle this on for presentation
os.chdir(r'C:\Users\trwi0358\Github\Pasture-Rangeland-Forage')
mask = readRaster("d:\\data\\droughtindices\\masks\\nad83\\mask4.tif",1,-9999)[0]

noaas, geom, proj = readRasters2("D:\\data\\droughtindices\\noaa\\nad83\\raw\\",-9999)
norays = [a[1] for a in noaas]
nomean = np.nanmean(norays,axis = 0)
toRaster(nomean,"g:\\my drive\\thesis\\data\\rasters\\mean_precip.tif",geom,proj)

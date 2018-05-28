# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 10:34:47 2018

@author: Travis
"""
############################ Get Functions ####################################
runfile('C:/Users/trwi0358/Github/Pasture-Rangeland-Forage/functions_git.py', 
        wdir='C:/Users/trwi0358/Github/Pasture-Rangeland-Forage')
# Read in Rasters
mask, geom, proj = readRaster(r'd:\data\droughtindices\masks\nad83\mask4.tif',1,-9999)
usdms = readRasters('d:\\data\\droughtindices\\usdm\\usdmrasters\\nad83\\all\\', -9999)[0]
usdms = [[a[0],a[1]*mask] for a in usdms]

# Combine weeks into monthly values and rename by month
# make list of usdms with monthless name strings
names = np.unique([a[0][:-2] for a in usdms])
usdmonths = [[[a[0][:-2],a[1]] for a in usdms if a[0][:-2] in names[i] or a[0][:-2] in names[i+1]] for i in range(len(names)-1)]
usdmonths = [a for a in usdmonths if a[0][0][-2:] != '12']

#usdmonths2 = [[month[0][0], np.nanmean([item[1] for item in month], axis = 0)] for month in usdmonths]
usdmonths2 = [[month[0][0], arrayMode([item[1] for item in month])] for month in tqdm(usdmonths)]

# Save to a folder in the d: drive
toRasters(usdmonths2,'d:\\data\\droughtindices\\usdm\\usdmrasters\\wgs\\usdmodes\\',geom,proj)
usdmodes = readRasters('d:\\data\\droughtindices\\usdm\\usdmrasters\\nad83\\usdmodes\\',-9999)[0]

#usdms, geo, proj = readRasters(r'E:\data\droughtindices\usdm\usdmrasters\nad83\index', -9999)

# Match the Probabilities and create new strike levels
# Save these strike values into the 3 types of strike levels csvs
# Original - No transformations
#indexHist(usdms,mostfreq = 'n')
#
## Standardized - Standardized to a 0 - 1 scale
#arrays = [usdms[i][1] for i in range(len(usdms))]
#amin = np.nanmin(arrays)
#amax = np.nanmax(arrays)
#indexlist = standardize(usdms,amin,amax)
#indexHist(indexlist)
## Reindexed - standardizeds and then reindexed by interval-wise average value
#indexlist = normalize(indexlist,1948,2016)            
#indexHist(indexlist,limmax = 4)

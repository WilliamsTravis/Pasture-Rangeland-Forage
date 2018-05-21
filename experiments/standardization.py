# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 09:14:36 2018

@author: trwi0358
"""

runfile('C:/Users/trwi0358/Github/Pasture-Rangeland-Forage/functions_git.py', wdir='C:/Users/trwi0358/Github/Pasture-Rangeland-Forage')
import warnings
warnings.filterwarnings("ignore") #This is temporary, toggle this on for presentation
os.chdir(r'C:\Users\trwi0358\Github\Pasture-Rangeland-Forage')
mask = readRaster("d:\\data\\droughtindices\\masks\\nad83\\mask4.tif",1,-9999)[0]

indices = ['D:\\data\\droughtindices\\noaa\\nad83\\monthlyindex\\',
 'D:\\data\\droughtindices\\palmer\\pdsi\\nad83\\',
 'D:\\data\\droughtindices\\palmer\\pdsisc\\nad83\\',
 'D:\\data\\droughtindices\\palmer\\pdsiz\\nad83\\',
 'D:\\data\\droughtindices\\spi\\nad83\\1month\\',
 'D:\\data\\droughtindices\\spi\\nad83\\2month\\',
 'D:\\data\\droughtindices\\spi\\nad83\\3month\\',
 'D:\\data\\droughtindices\\spi\\nad83\\6month\\',
 'D:\\data\\droughtindices\\spei\\nad83\\1month\\',
 'D:\\data\\droughtindices\\spei\\nad83\\2month\\',
 'D:\\data\\droughtindices\\spei\\nad83\\3month\\',
 'D:\\data\\droughtindices\\spei\\nad83\\6month\\']

def refineValues(rasterpath):
    # Get and set up raster values
    indexlist,geom,proj = readRasters2(rasterpath,-9999)
    
    # get index name
    indexname = indexlist[0][0][:-7]
    indexname = "".join([c.replace("-","").lower() for c in indexname])
        
    # Separate Rasters frome names
    arrays = [a[1] for a in indexlist]
    
    # Get standard deviation and adjust for outliers
    sd = np.nanstd(arrays)
    for a in arrays:
        a[a < -3*sd] = -3*sd
        a[a > 3*sd] = 3*sd
    
    # Reassign names
    indexlist = [[indexlist[i][0],arrays[i]] for i in range(len(indexlist))]
    
    # Standardize values
    indexlist = standardize(indexlist)
    
    # save raster to new folder
    toRasters(indexlist,rasterpath + "\\standardized_withoutliers\\",geom,proj)

for i in indices:
    refineValues(i)
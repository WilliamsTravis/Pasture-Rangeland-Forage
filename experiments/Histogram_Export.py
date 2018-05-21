# -*- coding: utf-8 -*-
"""

Creating histograms to export to R for ggplot. 
     R has a hard time generating these numbers, but the plot and graph theme
     used for the thesis is from ggplot.
     
     
Created on Thu Apr 19 15:13:29 2018

@author: trwi0358

"""
runfile('C:/Users/trwi0358/Github/Pasture-Rangeland-Forage/functions_git.py', wdir='C:/Users/trwi0358/Github/Pasture-Rangeland-Forage')
import warnings
warnings.filterwarnings("ignore") #This is temporary, toggle this on for presentation
os.chdir(r'C:\Users\trwi0358\Github\Pasture-Rangeland-Forage')
mask = readRaster("d:\\data\\droughtindices\\masks\\nad83\\mask4.tif",1,-9999)[0]

# Get and set up raster values
rasterpath = 'd:\\data\\droughtindices\\spei\\nad83\\2month\\'
rasterpath = 'd:\\data\\droughtindices\\noaa\\nad83\\indexvalues\\'

rasterpath = 'd:\\data\\droughtindices\\noaa\\nad83\\indexvalues\\'
rasterpath = 'd:\\data\\droughtindices\\palmer\\pdsiz\\nad83\\'
rasterpath = 'd:\\data\\droughtindices\\noaa\\nad83\\indexvalues\\'

# See what is should lool like
arrays = readRasters2(rasterpath,-9999)[0]
indexHist(array,binumber = 1000)

# Recreate for export
array = [ray[1] for ray in arrays]

# Get min and maximum values
amin = np.nanmin(array)
amax = np.nanmax(array)
amax = 4

# Knock off outliers
sd = np.nanstd(array)
for ray in array:
    ray[ray > 3*sd] = 3*sd
    ray[ray < -3*sd] = -3*sd

#arrays  = standardize(arrays)
# Needs to be masked?
array = np.ma.masked_invalid(array)

# Get histogram and bin values at 1000
hists,bins = np.histogram(array,range = [amin,amax],bins = 1000,normed = False)
bins = bins[:(len(bins)-1)]

# Export to CSV
histogram = pd.DataFrame(bins,hists)
histogram.to_csv("G:\\my drive\\thesis\\data\\index project\\SPEI2Histogram_noutliers.csv")

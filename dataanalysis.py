# -*- coding: utf-8 -*-
"""
To generate some summary statistics for the alternate index experiments

Created on Thu Mar 22 21:25:30 2018

@author: trwi0358
"""

# Collect modules and functions
runfile('C:/Users/trwi0358/Github/Pasture-Rangeland-Forage/functions_git.py', wdir='C:/Users/trwi0358/Github/Pasture-Rangeland-Forage')

# Read in two samples for context
rain = readRasters("d:\\data\\droughtindices\\noaa\\nad83\\indexvalues\\",-9999)[0]
rainst = standardize(rain)
indexHist(rain,limmax = 3)
indexHist(rainst,limmax =.1)
spei2 = readRasters("d:\\data\\droughtindices\\spei\\nad83\\2month\\",-9999)[0]
spei2st = standardize(spei2)
indexHist(spei2)
indexHist(spei2st)

# Read in the data frame
prfdf = pd.read_csv("G:\\My Drive\\THESIS\\data\\Index Project\\PRFIndex_specs.csv")
prfdf.index = prfdf['Drought Index']
prfdf = prfdf.drop(prfdf.columns[0],axis = 1)

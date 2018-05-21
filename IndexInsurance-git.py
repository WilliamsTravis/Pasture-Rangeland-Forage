# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 22:19:03 2017

This script allows you to change parameters and call the functions. The working directory is set in the functions script while this is being tinkered with. 
    
    
*** To check rain-index outputs for accuracy set the baseline years from 1948 to 2016 and check the matching outputs from this site:
    
    https://prodwebnlb.rma.usda.gov/apps/prf#
    
@author: Travis
"""
runfile('C:/Users/trwi0358/Github/Pasture-Rangeland-Forage/functions_git.py', wdir='C:/Users/trwi0358/Github/Pasture-Rangeland-Forage')
import warnings
warnings.filterwarnings("ignore") #This is temporary, toggle this on for presentation
os.chdir(r'C:\Users\trwi0358\Github\Pasture-Rangeland-Forage')
mask = readRaster("d:\\data\\droughtindices\\masks\\nad83\\mask4.tif",1,-9999)[0]

############### Argument Definitions ##########################################
actuarialyear = 2018
baselineyears = [1948,2016] 
studyears = [2000,2017]  
productivity = 1 
strike = .8
acres = 500
allocation = .5
difference = 0 # 0 = indemnities, 1 = net payouts, 2 = lossratios 

############################ Normal NOAA Method ###############################
rasterpath = "d:\\data\\droughtindices\\noaa\\nad83\\indexvalues\\"

# Function Call
[producerpremiums, indemnities, frequencies, 
 pcfs, nets, lossratios, meanppremium, 
 meanindemnity, frequencysum, meanpcf,
 net, lossratio] = indexInsurance(rasterpath, actuarialyear, studyears, baselineyears, 
                productivity, strike, acres, allocation,difference,
                plot = True) 

# Get rainfall stats   
noaas = [r[1] for r in indemnities]
nmean = np.nanmean(noaas)
nsum = np.nansum(noaas)
nmax = np.nanmax(noaas)

####################### Test methods for drought indices ######################
rasterpath = 'd:\\data\\droughtindices\\palmer\\pdsisc\\nad83\\'
rasterpath = 'd:\\data\\droughtindices\\spi\\nad83\\2month\\'

# Function Call
[producerpremiums, indemnities, frequencies, pcfs, nets, lossratios, meanppremium, meanindemnity, frequencysum, meanpcf, net, lossratio] = indexInsurance(rasterpath, actuarialyear, studyears, baselineyears, productivity, strike, acres, allocation,difference,plot = False) 

# Get Drought index stats
droughts = [r[1] for r in indemnities]
dmean = np.nanmean(droughts)
dsum = np.nansum(droughts)
dmax = np.nanmax(droughts)

################################# Compare General Stats #######################
nmean/dmean #spi6,.7: 1.75       .9: 1.64   |  spi1,.7: 1.67      .9: 1.67.......Same!
nsum/dsum  #spi6,.7: 1.71...?   .9: 1.60   |  spi1,.7: 1.62      .9: 1.63
nmax/dmax #spi6,.7: 1.23       .9: 1.24   |  spi1,.7: 1.13      .9: 1.13 .

# More indices
# SPEI
nmean/dmean #spei6,.7: 2.07     .9: 1.91  |  spei1,.7: 2.09     .9: 2.07........almost same!
nsum/dsum  #spei6,.7: 2.02     .9: 1.87  |  spei1,.7: 2.04     .9: 2.03 
nmax/dmax #spei6,.7: 1.61     .9: 1.56  |  spei1,.7: 1.66     .9: 1.60

# PDSI                                       # PDSIsc
nmean/dmean #pdsi,.7: 2.20    .9:  1.70  |  #pdsisc,.7: 1.87    .9: 1.77............close enough!
nsum/dsum  #pdsi,.7: 2.24    .9:  1.74  |  #pdsisc,.7: 1.90    .9: 1.79 
nmax/dmax #pdsi,.7: 1.38    .9:  1.36  |  #pdsisc,.7: 1.53    .9: 1.44 

# PDSI  z                                    
nmean/dmean #pdsiz,.7: 2.02    .9: 2.06..................................................almost same!
nsum/dsum  #pdsiz,.7: 2.06    .9: 2.09
nmax/dmax #pdsiz,.7: 1.30    .9: 1.29   

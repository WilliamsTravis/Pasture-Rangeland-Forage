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
filedir = 'd:\\data\\droughtindices\\'


############################ Set Projection ###################################
# nad83 or albers (epsg:4269 or epsg:102008)
proj = 'albers'
############################ Normal NOAA Method ###############################
rasterpath = "d:\\data\\droughtindices\\noaa\\"+proj+"\\raw"
#rasterpath = "f:\\data\\droughtindices\\noaa\\"+proj+"\\raw"
method = 1 # Method 1 is the present way of calculating triggers and magnitudes
adjustit = False
standardizeit = False
indexit = True

####################### Test methods for drought indices ######################
rasterpath = 'd:\\data\\droughtindices\\palmer\\pdsi\\nad83\\'
method = 2 # method 2 set strike levels based on matching probability of occurrence with the RMA index
adjustit = True
standardizeit = True
indexit = False

############### Argument Definitions ##########################################
actuarialyear = 2018
baselineyears = [1948,2016] 
studyears = [2000,2017]  
productivity = 1 
strike = .7
acres = 500
allocation = .5
difference = 0 # 0 = indemnities, 1 = net payouts, 2 = lossratios 


#################### Function Call #################################################################
[insurance_package_all, 
 insurance_package_average,#,cid,coords
 index_package_all,index_package] = indexInsurance(rasterpath, actuarialyear, studyears, baselineyears, productivity, strike, 
                             acres, allocation, adjustit = adjustit, standardizeit = standardizeit, 
                             indexit = indexit, method = method, difference = difference) 
# Return order:
#insurance_package_all = [producerpremiums,indemnities]
#insurance_package_average = [meanppremium,meanindemnity]
#index_package_all = [frequencyrays,pcfrays]
#index_package = [frequencysum,meanpcf]
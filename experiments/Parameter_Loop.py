# -*- coding: utf-8 -*-
"""
This will loop through all combinations of paramters for the online model and 
    save the average outputs as rasters, and pickle the time series for the 
    time series graphs

Created on Mon May  7 20:29:57 2018

@author: trwi0358
"""
runfile('C:/Users/trwi0358/Github/Pasture-Rangeland-Forage/functions_git.py', wdir='C:/Users/trwi0358/Github/Pasture-Rangeland-Forage')
import warnings
warnings.filterwarnings("ignore") #This is temporary, toggle this on for presentation
os.chdir(r'C:\Users\trwi0358\Github\Pasture-Rangeland-Forage')
mask, geom, proj = readRaster("d:\\data\\droughtindices\\masks\\nad83\\mask4.tif",1,-9999)

# Drought Index
paths = [
         'D:\\data\\droughtindices\\noaa\\nad83\\indexvalues\\',
         'D:\\data\\droughtindices\\palmer\\pdsi\\nad83\\',
         'D:\\data\\droughtindices\\palmer\\pdsisc\\nad83\\',
         'D:\\data\\droughtindices\\palmer\\pdsiz\\nad83\\',
         'D:\\data\\droughtindices\\spei\\nad83\\1month\\',
         'D:\\data\\droughtindices\\spei\\nad83\\2month\\',
         'D:\\data\\droughtindices\\spei\\nad83\\3month\\',
         'D:\\data\\droughtindices\\spei\\nad83\\6month\\',
         'D:\\data\\droughtindices\\spi\\nad83\\1month\\',
         'D:\\data\\droughtindices\\spi\\nad83\\2month\\',
         'D:\\data\\droughtindices\\spi\\nad83\\3month\\',
         'D:\\data\\droughtindices\\spi\\nad83\\6month\\'
         ]

indices = ["noaa","pdsi","pdsisc","pdsiz","spei1","spei2","spei3","spei6","spi1","spi2","spi3","spi6"]

# Strike level
strikes = [.7,.75,.8,.85,.9]

# Info Type
# producerpremiums,indemnities,frequencies,pcfs,nets, lossratios,meanppremium,meanindemnity,frequencysum,meanpcf, net, lossratio
infotype = [i for i in range(6,12)]

# Actuarial Year
actuarialyears  = [2017,2018]

# Number of Acres....uh oh...better make this discrete
acres = [250,500,1000,2000]

# rasterpath, actuarialyear, studyears, baselineyears, productivity, strike, acres, allocation,difference = 0, scale = True,plot = True
for p in range(len(paths)):
    print(paths[p])
    for ay in actuarialyears:
        print(ay)
        for s in strikes:
            print(s)
            df = indexInsurance(paths[p], # Index Path
                                ay, # Actuarial Year
                                [2017,2018], # Study years
                                [1948,2017], # Baseline
                                1, # Productivity
                                s, # Strike
                                500, # Acres
                                .5, # Allocation
                                scale = True,plot = False)
#            returns = producerpremiums,indemnities,frequencies,pcfs,nets, lossratios,meanppremium,meanindemnity,frequencysum,meanpcf, net, lossratio
            # Premiums
            toRaster(df[6],
                     "C:\\Users\\trwi0358\\Github\\Pasture-Rangeland-Forage\\data\\onlinedata\\AY"+str(ay)+"\\"+str(int(s*100))+"\\premiums\\"+indices[p]+"\\raster.tif",
                     geom,proj)
            
            array = open("C:\\Users\\trwi0358\\Github\\Pasture-Rangeland-Forage\\data\\onlinedata\\AY"+str(ay)+"\\"+str(int(s*100))+"\\premiums\\"+indices[p]+"\\arrays.pickle",'wb')
            pickle.dump(df[0], array)
           
            # Indemnities
            toRaster(df[7],
                     "C:\\Users\\trwi0358\\Github\\Pasture-Rangeland-Forage\\data\\onlinedata\\AY"+str(ay)+"\\"+str(int(s*100))+"\\indemnities\\"+indices[p]+"\\raster.tif",
                     geom,proj)
            
            array = open("C:\\Users\\trwi0358\\Github\\Pasture-Rangeland-Forage\\data\\onlinedata\\AY"+str(ay)+"\\"+str(int(s*100))+"\\indemnities\\"+indices[p]+"\\arrays.pickle",'wb')
            pickle.dump(df[1], array)
            
            # frequencies
            toRaster(df[8],
                     "C:\\Users\\trwi0358\\Github\\Pasture-Rangeland-Forage\\data\\onlinedata\\AY"+str(ay)+"\\"+str(int(s*100))+"\\frequencies\\"+indices[p]+"\\raster.tif",
                     geom,proj)
            
            array = open("C:\\Users\\trwi0358\\Github\\Pasture-Rangeland-Forage\\data\\onlinedata\\AY"+str(ay)+"\\"+str(int(s*100))+"\\frequencies\\"+indices[p]+"\\arrays.pickle",'wb')
            pickle.dump(df[2], array)
            
            # pcfs
            toRaster(df[9],
                     "C:\\Users\\trwi0358\\Github\\Pasture-Rangeland-Forage\\data\\onlinedata\\AY"+str(ay)+"\\"+str(int(s*100))+"\\pcfs\\"+indices[p]+"\\raster.tif",
                     geom,proj)
            
            array = open("C:\\Users\\trwi0358\\Github\\Pasture-Rangeland-Forage\\data\\onlinedata\\AY"+str(ay)+"\\"+str(int(s*100))+"\\pcfs\\"+indices[p]+"\\arrays.pickle",'wb')
            pickle.dump(df[3], array)

            # nets
            toRaster(df[10],
                     "C:\\Users\\trwi0358\\Github\\Pasture-Rangeland-Forage\\data\\onlinedata\\AY"+str(ay)+"\\"+str(int(s*100))+"\\nets\\"+indices[p]+"\\raster.tif",
                     geom,proj)
            
            array = open("C:\\Users\\trwi0358\\Github\\Pasture-Rangeland-Forage\\data\\onlinedata\\AY"+str(ay)+"\\"+str(int(s*100))+"\\nets\\"+indices[p]+"\\arrays.pickle",'wb')
            pickle.dump(df[4], array)
            
            # nets
            toRaster(df[11],
                     "C:\\Users\\trwi0358\\Github\\Pasture-Rangeland-Forage\\data\\onlinedata\\AY"+str(ay)+"\\"+str(int(s*100))+"\\lossratios\\"+indices[p]+"\\raster.tif",
                     geom,proj)
            
            array = open("C:\\Users\\trwi0358\\Github\\Pasture-Rangeland-Forage\\data\\onlinedata\\AY"+str(ay)+"\\"+str(int(s*100))+"\\lossratios\\"+indices[p]+"\\arrays.pickle",'wb')
            pickle.dump(df[5], array)
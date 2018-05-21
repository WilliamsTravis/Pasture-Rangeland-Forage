# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 14:39:02 2018

@author: trwi0358
"""
runfile('C:/Users/trwi0358/Github/Pasture-Rangeland-Forage/functions_git.py', wdir='C:/Users/trwi0358/Github/Pasture-Rangeland-Forage')
import warnings
warnings.filterwarnings("ignore") #This is temporary, toggle this on for presentation
os.chdir(r'C:\Users\trwi0358\Github\Pasture-Rangeland-Forage')
mask = readRaster("d:\\data\\droughtindices\\masks\\nad83\\mask4.tif",1,-9999)[0]

# Index paths
indices = [
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

# Index names for the table
indexnames = {
          'D:\\data\\droughtindices\\noaa\\nad83\\indexvalues\\': 'NOAA',
          'D:\\data\\droughtindices\\palmer\\pdsi\\nad83\\': 'PDSI',
          'D:\\data\\droughtindices\\palmer\\pdsisc\\nad83\\': 'PDSIsc',
          'D:\\data\\droughtindices\\palmer\\pdsiz\\nad83\\': 'PDSIz',
          'D:\\data\\droughtindices\\spei\\nad83\\1month\\': 'SPEI-1', 
          'D:\\data\\droughtindices\\spei\\nad83\\2month\\': 'SPEI-2', 
          'D:\\data\\droughtindices\\spei\\nad83\\3month\\': 'SPEI-3', 
          'D:\\data\\droughtindices\\spei\\nad83\\6month\\': 'SPEI-6',
          'D:\\data\\droughtindices\\spi\\nad83\\1month\\':'SPI-1',
          'D:\\data\\droughtindices\\spi\\nad83\\2month\\':'SPI-2',
          'D:\\data\\droughtindices\\spi\\nad83\\3month\\':'SPI-3',
          'D:\\data\\droughtindices\\spi\\nad83\\6month\\':'SPI-6'
          }
averages = []

strikes = [.7,.75,.8,.85,.9]
studyears = [1948,2017]
baselineyears = studyears
actuarialyear = 2018
productivity = 1
acres = 500
allocation = .5
difference = 1


for i in range(len(indices)):
    for s in range(len(strikes)):
        indexname = indexnames.get(indices[i])
        print(indexname)
        # Function Call
        [producerpremiums, indemnities, 
         frequencies, pcfs, nets, lossratios,
         meanppremium, meanindemnity, 
         frequencysum, meanpcf, net, lossratio] = indexInsurance(indices[i], actuarialyear, studyears, baselineyears, 
                     productivity, strikes[s], acres, allocation,difference,scale = True,plot = False) 
        
        # Get Drought index stats
        droughts = [r[1] for r in indemnities]
        dmean = np.nanmean(droughts)
    
        #add to list
        averages.append([indexname, strikes[s] , dmean])
        
avdf = pd.DataFrame(averages)
avdf.columns = ['index','strike','meanpayment']
avdf.to_csv("G:/my drive/thesis/data/Index Project/PRF_meanpayments_scaled.csv")
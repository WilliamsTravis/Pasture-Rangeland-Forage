# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 12:47:52 2018

Collecting all the information from each index and set of parameters

@author: trwi0358
"""
runfile('C:/Users/trwi0358/Github/Pasture-Rangeland-Forage/functions_git.py', wdir='C:/Users/trwi0358/Github/Pasture-Rangeland-Forage')
import warnings
import pysal as pys
warnings.filterwarnings("ignore") #This is temporary, toggle this on for presentation
os.chdir(r'C:\Users\trwi0358\Github\Pasture-Rangeland-Forage')
mask = readRaster("d:\\data\\droughtindices\\masks\\nad83\\mask4.tif",1,-9999)[0]
grid = readRaster("d:\\data\\droughtindices\\rma\\nad83\\prfgrid.tif",1,-9999.)[0]

# Establish parameters lists.
# Index paths
indices = ['D:\\data\\droughtindices\\noaa\\nad83\\indexvalues\\',
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

# Index names for the table
indexnames = {'D:\\data\\droughtindices\\noaa\\nad83\\indexvalues\\': 'NOAA',
            'D:\\data\\droughtindices\\palmer\\pdsi\\nad83\\': 'PDSI',
          'D:\\data\\droughtindices\\palmer\\pdsisc\\nad83\\': 'PDSIsc',
          'D:\\data\\droughtindices\\palmer\\pdsiz\\nad83\\': 'PDSIz',
          'D:\\data\\droughtindices\\spi\\nad83\\1month\\':'SPI-1',
          'D:\\data\\droughtindices\\spi\\nad83\\2month\\':'SPI-2',
          'D:\\data\\droughtindices\\spi\\nad83\\3month\\':'SPI-3',
          'D:\\data\\droughtindices\\spi\\nad83\\6month\\':'SPI-6',
          'D:\\data\\droughtindices\\spei\\nad83\\1month\\': 'SPEI-1', 
          'D:\\data\\droughtindices\\spei\\nad83\\2month\\': 'SPEI-2', 
          'D:\\data\\droughtindices\\spei\\nad83\\3month\\': 'SPEI-3', 
          'D:\\data\\droughtindices\\spei\\nad83\\6month\\': 'SPEI-6'}

# Lists of other parameters
actuarialyear = [2017,2018]
baselineyears = [[1948,2016],[1968,2016],
                 [1988,2016], [2008,2016]]
studyears = [[1948,2017],[1968,2017],
             [1988,2017], [2008,2017]] 
#productivities = [.6,1,1.5] 
strikes = [.7,.75,.8,.85,.9]
#acres = [500,1000,1500] # Effects would be linear I think, might as well just in case.
allocation = .5 # This seems odd to vary to me, effects would be linear

# Column names
columns = ["Drought Index",
           "Actuarial Year",
           "Index COV",
           "Strike",
           "Baseline Range",
           "Study Range",
           "Temporal Scale",
           "Max Payment",
           "Minimum Payment",
           "Median Payment",
           "Mean Payment",
           "Payment SD",
           "Monthly Payment SD",
           "Mean PCF",
           "PCF SD",
           "Monthly PCF SD",
           "Mean Payout Frequency",
           "Monthly Payout Frequency SD"]
    
# Empty Data Frame
prfdf = pd.DataFrame(columns = columns)

# Iteratively call every parameter to generate prfdf rows. Could take a minute, 
    # This gives us 235,200 iterations :D
#prfdf = pd.read_csv("G:\\My Drive\\THESIS\\data\\Index Project\\PRFIndex_specs.csv")
iteration = len(prfdf.index)
totaliterations = len(indices)*len(actuarialyear)*len(baselineyears)*len(studyears)*len(strikes)

# I am taking out the other baseline years for now. It is meaningless for anything but the rainfall index
baselineyears = [[1948, 2017]]
for by in baselineyears:
    print("Choosing basline years...")
    for i in indices:
        prfdf.to_csv("G:\\My Drive\\THESIS\\data\\Index Project\\PRFIndex_specs.csv")
        print(i)
        indexlist = readRasters2(i,-9999)[0]
        indexlist = [[a[0],a[1]*mask] for a in indexlist]
        indexcov = c*12 # what happened here? that c is probably from the covCellwise function, but *12? 
        ovCellwise(indexlist)
        name = indexnames.get(i)                            
        if name == "NOAA":
            indexlist = normalize(indexlist,by[0],by[1])
            categorypath = None

        else:
            indexlist = adjustIntervals(indexlist)
            arrays = [indexlist[i][1] for i in range(len(indexlist))]
            indexlist = standardize(indexlist)
            categorypath = 'data\\Index Categories\\indexcategories-standardized.csv'
        for ay in actuarialyear:
            print("Bundling Actuarials...Year: "+str(ay))
            if ay == 2017:
                actuarialpath = 'data\\actuarial\\2017\\rasters\\nad83\\'
            elif ay == 2018:
                actuarialpath = 'data\\actuarial\\2018\\rasters\\nad83\\'
            premiumpath = actuarialpath+'premiums\\'
            basepath = actuarialpath+'bases\\rates\\'
            allocationminpath = actuarialpath+'bases\\allocations\\min\\'
            allocationmaxpath = actuarialpath+'bases\\allocations\\max\\'
            premiums = readRasters2(premiumpath,-9999.)[0] #[0] because we can use the original geometry to write these to rasters.     
            bases = readRasters2(basepath,-9999.)[0]     
            allocmins = readRasters2(allocationminpath,-9999.)[0]
            allocmaxes = readRasters2(allocationmaxpath,-9999.)[0] 
            actuarial_bundle = [premiums,bases,allocmins,allocmaxes]
            for sy in studyears:
                indexlist = [year for year in indexlist if int(year[0][-6:-2]) >= sy[0] and int(year[0][-6:-2]) <= sy[1]]
                print("Choosing Study Years..." + str(sy))
                for s in strikes:
                    print("Choosing Strike Level..." + str(s))
                    iteration += 1 
                    print("Building Dataset...")
                    data = indexInsurance2(indexlist, actuarial_bundle, categorypath, 
                                          1, s, 500, allocation) 
                    strike = s
                    baserange = by[1] - by[0]
                    studyrange = sy[1] - sy[0]
                    if "-" in name:
                        scale = int(name[-1:])
                    elif  "z" in name or name == 'NOAA':
                        scale = 1
                    else:
                        scale = np.nan
                    maxpay = np.nanmax(data[7])
                    minpay = np.nanmin(data[7])
                    medpay = np.nanmedian(data[7])
                    meanpay = np.nanmean(data[7])
                    paysd = np.nanstd(data[7]) # Standard Deviation in payments between locations
                    monthpaysd = monthlySD(data[1]) # Standard Deviation between monthly cell-wise average payments
                    meanpcf = np.nanmean(data[9]) 
                    pcfsd = np.nanstd(data[9]) # Standard Deviation in PCFs bwetween locations
                    monthpcfsd = monthlySD(data[3]) # Standard Deviation between monthly cell-wise average PCFs
                    meanfre = np.nanmean(data[8])
                    fresd = np.nanstd(data[8]) # Standard Deviation in payouts between locations
                    monthfresd = monthlySD2(data[2]) # Standard Deviation between monthly cell-wise average payout frequencies
                    
                    # Create a row for the df! Pay attention to order
                    print("Appending to dataframe...")
                    row = [name,ay,indexcov,strike, baserange,studyrange,scale,maxpay,minpay,medpay,meanpay,
                           paysd,monthpaysd,meanpcf,pcfsd,monthpcfsd,meanfre,monthfresd]
                    rowdict = dict(zip(columns,row))
                    prfdf = prfdf.append(rowdict,ignore_index=True)
                    print(str(iteration) + " / " + str(totaliterations) +"  |  " + str(round(iteration/totaliterations,2)*100) + "%")

prfdf.to_csv("C:\\Users\\trwi0358\\Github\\Pasture-Rangeland-Forage\\data\\PRFIndex_specs.csv")
prfdf_original = pd.read_csv("C:\\Users\\trwi0358\\Github\\Pasture-Rangeland-Forage\\data\\PRFIndex_specs_original.csv")

prfdf = pd.read_csv("C:\\Users\\trwi0358\\Github\\Pasture-Rangeland-Forage\\data\\PRFIndex_specs.csv")
prfdf.columns = prfdf_original.columns

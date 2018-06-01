# -*- coding: utf-8 -*-
"""
Created on Fri May 25 15:52:52 2018

Loop through each state and get our basis risk assessment.

@author: trwi0358
"""

############################ Get Functions ####################################
runfile('C:/Users/user/Github/Pasture-Rangeland-Forage/functions_git.py', 
        wdir='C:/Users/user/Github/Pasture-Rangeland-Forage')

############################ Get Payout Rasters ###############################
import warnings
warnings.filterwarnings("ignore") 
os.chdir("c:\\users\\user\\github\\pasture-rangeland-forage")
source = xr.open_rasterio("e:\\data\\droughtindices\\rma\\nad83\\prfgrid.tif")
source_signal = '["e:\\\\data\\\\droughtindices\\\\noaa\\\\nad83\\\\indexvalues\\\\", 4, 0.7,100]'
grid,geom,proj = readRaster('data\\rma\\nad83\\prfgrid.tif',1,-9999)
strike = .7
mask = readRaster('e:\\data\\droughtindices\\masks\\nad83\\mask4.tif',1,-9999)[0]
# Load pre-conditioned bi-monthly USDM modal category rasters into numpy arrays
#usdmodes = readRasters("D:\\data\\droughtindices\\usdm\\usdmrasters\\nad83\\usdmeans\\",-9999)[0]
usdmodes = readRasters("e:\\data\\droughtindices\\usdm\\usdmrasters\\nad83\\usdmodes\\",-9999)[0]
indexlist = readRasters('e:\\data\\droughtindices\\noaa\\nad83\\indexvalues\\',-9999)[0]
################################# Save Numoy arrays to compressed files #######
#udates = [a[0] for a in usdmodes]
#justdates = [a[-6:] for a in udates]
#usdmodes = [a[1] for a in usdmodes]
#indexlist = [a for a in indexlist if a[0][-6:] in justdates]
#np.savez_compressed("E:\\data\\prf-usdm\\usdm\\usdm_arrays",usdmodes)
#np.savez_compressed("E:\\data\\prf-usdm\\usdm\\usdm_dates",udates)



statefps = pd.read_csv("data\\statefps.csv")
states = readRaster("data\\usacontiguous.tif",1,-9999)[0] 
statedict = dict(zip(statefps['statefp'],statefps['state']))
dfcols = ["state","strike","dm","missed_sum","missed_ratio","strike_events", "dm_events"]
dfrm = pd.DataFrame(columns = dfcols)
for s in tqdm(statefps['statefp']):
    state = statedict.get(s)
    statecopy = np.copy(states)
    for dm in [0,1,2,3,4]:
        for strike in [.7,.75,.8,.85,.9]:
            statelocs = np.where(statecopy == s)
            statecopy[statelocs] = 999
            statecopy[statecopy < 999] = np.nan
            statemask = statecopy*0+1
            udates = [m[0][-6:] for m in usdmodes]
            indexlist = [i for i in indexlist if i[0][-6:] in udates]
            idates = [m[0][-6:] for m in indexlist]
            usdms = [u for u in usdmodes if u[0][-6:] in idates]
            
            # Create a list of monthly arrays with 1's for the scenario
            risks = [basisCheck(usdm = usdms[i],noaa = indexlist[i],strike = strike, dm = dm) for i in range(len(usdms))]
            
            # Sum them up
            hits = np.nansum(risks,axis = 0)*mask
        #    hits[hits==0]  = .01
        
            # Create a list of monthly arrays with 1's for droughts
            droughts = [droughtCheck(usdm = usdmodes[i],dm = dm) for i in range(len(usdmodes))]
        #    droughtchances[droughtchances == 0] = 1000
            rainbelow = [droughtCheck2(rain = indexlist[i],strike = strike) for i in range(len(indexlist))]
        
            # Sum and divide by time steps
            droughtchances = np.nansum(droughts,axis = 0)*mask
            rainchance = np.nansum(rainbelow,axis = 0)*mask
            
            
            # Final Basis risk according to the USDM and Muneepeerakul et als method
            basisrisk = hits/droughtchances
            
            basisrisk = basisrisk*statemask
            droughtchances = droughtchances*statemask
            hits = hits*statemask
            rainchance = rainchance*statemask
            
            # Get Risk number for each 
#            riskratio = np.nanmean(basisrisk)
            riskratio = np.nansum(droughtchances*basisrisk)/np.nansum(droughtchances)
            risksum = np.nansum(hits)
            strike_events = np.nansum(rainchance)
            dm_events = np.nansum(droughtchances)
            row = [state,strike,"D"+str(dm),risksum,riskratio, strike_events, dm_events]
            row = dict(zip(dfcols,row))
            # Append to df
            dfrm = dfrm.append(row,ignore_index = True)
dfrm2 = dfrm
dfrm3 = dfrm
dfrm['missed_ratio'] = round(dfrm['missed_ratio'],2)       
dfrm = dfrm.replace(0,np.nan) 
dfrm.to_csv("data\\state_risks.csv")
            

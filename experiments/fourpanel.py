# -*- coding: utf-8 -*-
"""
A four panel sample of payouts at particular locations

Created on Wed May  2 20:26:19 2018

@author: trwi0358
"""
runfile('C:/Users/trwi0358/Github/Pasture-Rangeland-Forage/functions_git.py', wdir='C:/Users/trwi0358/Github/Pasture-Rangeland-Forage')
import warnings
warnings.filterwarnings("ignore") #This is temporary, toggle this on for presentation
os.chdir(r'C:\Users\trwi0358\Github\Pasture-Rangeland-Forage')
mask = readRaster("d:\\data\\droughtindices\\masks\\nad83\\mask4.tif",1,-9999)[0]
grid = readRaster("d:\\data\\droughtindices\\rma\\nad83\\prfgrid.tif",1,-9999)[0]
############### Argument Definitions ##########################################
actuarialyear = 2018
baselineyears = [1948,2016] 
studyears = [2000,2017]  
productivity = 1 
strike = .8
acres = 500
allocation = .5

############################ Normal NOAA Method ###############################

rasterpath1 = "d:\\data\\droughtindices\\noaa\\nad83\\indexvalues\\"
rasterpath2 = "d:\\data\\droughtindices\\spi\\nad83\\6month\\"
#rasterpath2 = "d:\\data\\droughtindices\\palmer\\pdsi\\nad83\\"
#rasterpath2 = "d:\\data\\droughtindices\\spei\\nad83\\6month\\"
index = 'spi6'
# Function Call
# Return order:
#    producerpremiums, indemnities, frequencies, pcfs, nets, lossratios, 
#    meanppremium, meanindemnity, frequencysum, meanpcf, net, lossratio
noaas= indexInsurance(rasterpath1, actuarialyear, studyears, baselineyears, productivity, strike, acres, allocation,scale = True,plot = False) 
spei1s= indexInsurance(rasterpath2, actuarialyear, studyears, baselineyears, productivity, strike, acres, allocation,scale = True,plot = False) 


############################## Time Series ####################################
if len(noaas[0]) < len(spei1s[0]):
    shorter = noaas
else:
    shorter = spei1s
ndates = [a[0][-6:-2]+"-"+a[0][-2:] for a in shorter[0]]

# get frequencies 
pcfs_n = noaas[1]
pcfs_n = [a[1] for a in pcfs_n[:len(ndates)]]
pcfs_s = spei1s[1]
pcfs_s = [a[1] for a in pcfs_s[:len(ndates)]]

# Billings, MT 
grid_loc = np.where(grid == 30986)
mt_n = [float(pcf[grid_loc]) for pcf in pcfs_n]
mt_s = [float(pcf[grid_loc]) for pcf in pcfs_s]

# Coleman, TX 
grid_loc = np.where(grid == 14223)
tx_n = [float(pcf[grid_loc]) for pcf in pcfs_n]
tx_s = [float(pcf[grid_loc]) for pcf in pcfs_s]

# Kearney, NE 
grid_loc = np.where(grid == 24724)
ne_n = [float(pcf[grid_loc]) for pcf in pcfs_n]
ne_s = [float(pcf[grid_loc]) for pcf in pcfs_s]

# Oklahoma
grid_loc = np.where(grid == 18430)
ok_n = [float(pcf[grid_loc]) for pcf in pcfs_n]
ok_s = [float(pcf[grid_loc]) for pcf in pcfs_s]

################################# Make Data Frame #############################
df_n = pd.DataFrame([mt_n, tx_n,ne_n,ok_n])
df_n.columns = ndates
df_n['index'] = ["rainfall","rainfall","rainfall","rainfall"]

df_s = pd.DataFrame([mt_s, tx_s,ne_s,ok_s])
df_s.columns = ndates
df_s['index'] = list(np.repeat(index,4))

locations = np.tile(["MT","TX","NE","OK"],2)

df = pd.concat([df_n,df_s])
df['location'] = locations
df = df.reset_index()

df.to_csv(r"G:\My Drive\THESIS\data\Index Project\fourpanel_SPI6.csv")

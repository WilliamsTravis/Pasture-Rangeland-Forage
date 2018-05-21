# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 20:43:15 2018

@author: trwi0358
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 16:32:09 2018

@author: trwi0358
"""
runfile('C:/Users/trwi0358/Github/Pasture-Rangeland-Forage/functions_git.py', 
        wdir='C:/Users/trwi0358/Github/Pasture-Rangeland-Forage')
names = ["pdsi", "pdsisc", "pdsiz", "spi1","spi2","spi3", "spi6", "spei1",
         "spei2","spei3","spei6" ]
noaapath = 'D:\\data\\droughtindices\\noaa\\nad83\\indexvalues\\'
paths= ['D:\\data\\droughtindices\\palmer\\pdsi\\nad83\\',
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
                
############### Argument Definitions ##########################################
actuarialyear = 2018
baselineyears = [1948,2016] 
studyears = [2000,2017]  
productivity = 1 
strikes = [.7,.75,.8,.85,.9]
acres = 500
allocation = .5
difference = 0 # 0 = indemnities, 1 = net payouts, 2 = lossratios 

############################ Normal NOAA Method ###############################
noaas = []
for i in range(len(strikes)):
    [producerpremiums, indemnities, frequencies, pcfs, nets, 
     lossratios, meanppremium, meanindemnity, frequencysum,
     meanpcf, net, lossratio] = indexInsurance(noaapath, actuarialyear, 
     studyears, baselineyears, productivity, strikes[i], acres, allocation,
     difference,scale = True,plot = False) 

    payments = [n[1] for n in indemnities]
    noaas.append(np.nanmean(payments))

noaamean = np.mean(noaas)

####################### Test methods for drought indices ######################
# Step one, scalar one
#ratios = []
#for i in range(len(paths)):   
#    print(names[i])  
#    # Step one, scalar one -- strike level ratios   
#    levels = []   
#    for s in range(len(strikes)):
#        # Get payouts at this strike level
#        [producerpremiums, indemnities, frequencies, pcfs, nets, 
#             lossratios, meanppremium, meanindemnity, frequencysum,
#             meanpcf, net, lossratio] = indexInsurance(paths[i], 
#             actuarialyear, studyears, baselineyears, productivity, 
#             strikes[s], acres, allocation,difference,
#             scale = False,plot = False) 
#        
#        # Get just the payouts at this strike level
#        payments = [n[1] for n in indemnities]
#        
#        # Get the ratio between payouts at this strike level and the rainfall one
#        ratio = noaas[s][2] / np.nanmean(payments)
#        
#        # Add the mean payout and total ratio to the full levels set
#        levels.append([strikes[s],np.nanmean(payments), ratio])
#        
#    # Get the average ratio between all strike levels
#    justratios = [l[2] for l in levels]    
#    meanratio = np.mean(justratios)
#    ratios.append(meanratio)
#scalars = pd.DataFrame([[names[i],ratios[i]] for i in range(len(ratios))])
#scalars.columns = ["index","ratio"]
#scalars.to_csv("G:\\My Drive\\THESIS\\data\\Index Project\\index_ratios.csv",index=False)


# Step two, scalar two
ratios2 = []
for i in range(len(paths)):   
    print(names[i]) 
    # Now we need to adjust for total payouts. 
    totals = []
    for s in range(len(strikes)):
        [producerpremiums, indemnities, frequencies, pcfs, nets, 
             lossratios, meanppremium, meanindemnity, frequencysum,
             meanpcf, net, lossratio] = indexInsurance(paths[i], 
             actuarialyear, studyears, baselineyears, productivity, 
             strikes[s], acres, allocation,difference,
             scale = True,plot = False) 
        
        # Get each payout set, multiply by the scalar and add mean to totals list
        payments = [n[1] for n in indemnities]
        totalmean = np.nanmean(payments)
        totals.append(totalmean)
     
    # Get average of totals and get ratio between noaamean
    totalratio = noaamean / np.nanmean(totals)
    ratios2.append([names[i],totalratio])
        
        
        
ratios2.sort()
names.sort()
scalars2 = pd.DataFrame([[ratios2[i][0],ratios2[i][1]] for i in range(len(ratios))])
scalars2.columns = ["index","ratio"]
scalars2.to_csv("G:\\My Drive\\THESIS\\data\\Index Project\\index_ratios2.csv",index=False)

scalars1 = pd.read_csv("G:\\my drive\\thesis\\data\\Index Project\\index_ratios.csv")

scalars1.index = scalars1['index']
scalars2.index = scalars2['index']
scalars = scalars1.join(scalars2,lsuffix='ratio1', rsuffix='ratio2')

scalars = scalars.drop(['indexratio2'],axis = 1)
scalars.columns = ["index","ratio1","ratio2"]
scalars['ratio'] = scalars['ratio1']*scalars['ratio2']

scalars.to_csv("G:\\My Drive\\THESIS\\data\\Index Project\\index_ratios.csv",index=False)









####################### PDSIs ################################################
palmers = []
for i in range(2):
    means = []
    for s in range(len(strikes)):
        [producerpremiums, indemnities, frequencies, pcfs, nets, 
         lossratios, meanppremium, meanindemnity, frequencysum,
         meanpcf, net, lossratio] = indexInsurance(palmerpaths[i],
         actuarialyear, studyears, baselineyears, productivity, strikes[s], 
         acres, allocation,difference,scale = False,plot = False) 

        payments = [n[1] for n in indemnities]
        ratio = noaas[s][2] / np.nanmean(payments)
        means.append([strikes[s],np.nanmean(payments), ratio])
    palmers.append(levels)
    
alltogether = [item for sublist in palmers for item in sublist]   
justratios = [p[2] for p in alltogether]
thepalmeratio = np.mean(justratios)
    
####################### PDSIz ################################################
zs = []
for s in range(len(strikes)):
    [producerpremiums, indemnities, frequencies, pcfs, nets, 
     lossratios, meanppremium, meanindemnity, frequencysum,
     meanpcf, net, lossratio] = indexInsurance(palmerpaths[2], actuarialyear, 
     studyears, baselineyears, productivity, strikes[s], acres, allocation,
     difference,scale = False,plot = False) 

    payments = [n[1] for n in indemnities]
    ratio = noaas[s][2] / np.nanmean(payments)
    zs.append([strikes[s],np.nanmean(payments), ratio])
    
justratios = [p[2] for p in zs]
thezratio = np.mean(justratios)  
####################### SPI ################################################
spis = []
for i in range(len(spipaths)):
    levels = []
    for s in range(len(strikes)):
        [producerpremiums, indemnities, frequencies, pcfs, nets, 
         lossratios, meanppremium, meanindemnity, frequencysum,
         meanpcf, net, lossratio] = indexInsurance(spipaths[i], actuarialyear, 
         studyears, baselineyears, productivity, strikes[s], acres, allocation,
         difference,scale = False,plot = False) 
    
        payments = [n[1] for n in indemnities]
        ratio = noaas[s][2] / np.nanmean(payments)
        levels.append([strikes[s],np.nanmean(payments), ratio])
    spis.append(levels)
    
alltogether = [item for sublist in spis for item in sublist]   
justratios = [p[2] for p in alltogether]
thespiratio = np.mean(justratios)
    
####################### SPEI ################################################
speis = []
for i in range(len(speipaths)):
    levels = []
    for s in range(len(strikes)):
        [producerpremiums, indemnities, frequencies, pcfs, nets, 
         lossratios, meanppremium, meanindemnity, frequencysum,
         meanpcf, net, lossratio] = indexInsurance(speipaths[i], actuarialyear,
         studyears, baselineyears, productivity, strikes[s], acres, allocation,
         difference,scale = False,plot = False) 

        payments = [n[1] for n in indemnities]
        ratio = noaas[s][2] / np.nanmean(payments)
        levels.append([strikes[s],np.nanmean(payments), ratio])
    speis.append(levels)
    
alltogether = [item for sublist in speis for item in sublist]   
justratios = [p[2] for p in alltogether]
thespeiratio = np.mean(justratios)

############ Save to File ###################################################
# Create dataframes for each to show this step
# NOAA
ratios = []
payments = []
for s in range(len(strikes)):
    ratios.append(1)
    payments.append(noaas[s][2])
nstrikes = pd.DataFrame(strikes)
name =pd.DataFrame(np.repeat(["noaa"],len(strikes))) 
ratiodf = pd.DataFrame(ratios).stack()
paymentdf = pd.DataFrame(payments).stack()
noaadf = pd.concat([name,ratiodf.reset_index(drop=True), paymentdf.reset_index(drop=True),nstrikes], axis=1)
noaadf.columns = ["index","ratio","payment","strike"]

# PDSIs
pdsiratios = []
pdsipayments = []
for sp in range(len(palmers)):
    ratios = []
    payments = []
    for s in range(len(strikes)):
        ratios.append(palmers[sp][s][2])
        payments.append(palmers[sp][s][1])
    pdsiratios.append(ratios)
    pdsipayments.append(payments)
    
pdsistrikes = pd.DataFrame(np.tile(strikes,len(palmers)))
pdsinames =pd.DataFrame(np.repeat(["pdsi","pdsisc"],len(strikes))) 
ratiodf = pd.DataFrame(pdsiratios).stack()
paymentdf = pd.DataFrame(pdsipayments).stack()

pdsidf = pd.concat([pdsinames,ratiodf.reset_index(drop=True), paymentdf.reset_index(drop=True),pdsistrikes], axis=1)
pdsidf.columns = ["index","ratio","payment","strike"]

# PDSIZ
zratios = []
zpayments = []
for s in range(len(strikes)):
    zratios.append(zs[s][2])
    zpayments.append(zs[s][1])
zstrikes = pd.DataFrame(strikes)
zname =pd.DataFrame(np.repeat(["pdsiz"],len(strikes))) 
ratiodf = pd.DataFrame(zratios).stack()
paymentdf = pd.DataFrame(zpayments).stack()
zdf = pd.concat([zname,ratiodf.reset_index(drop=True), paymentdf.reset_index(drop=True),zstrikes], axis=1)
zdf.columns = ["index","ratio","payment","strike"]

# SPEI
speiratios = []
speipayments = []
for sp in range(len(speis)):
    ratios = []
    payments = []
    for s in range(len(strikes)):
        ratios.append(speis[sp][s][2])
        payments.append(speis[sp][s][1])
    speiratios.append(ratios)
    speipayments.append(payments)
    
speistrikes = pd.DataFrame(np.tile(strikes,len(speis)))
speinames =pd.DataFrame(np.repeat(["spei1","spei2","spei3","spei6"],len(strikes))) 
ratiodf = pd.DataFrame(speiratios).stack()
paymentdf = pd.DataFrame(speipayments).stack()

speidf = pd.concat([speinames,ratiodf.reset_index(drop=True), paymentdf.reset_index(drop=True),speistrikes], axis=1)
speidf.columns = ["index","ratio","payment","strike"]

# SPI
spiratios = []
spipayments = []
for sp in range(len(spis)):
    ratios = []
    payments = []
    for s in range(len(strikes)):
        ratios.append(spis[sp][s][2])
        payments.append(spis[sp][s][1])
    spiratios.append(ratios)
    spipayments .append(payments)
    
spistrikes = pd.DataFrame(np.tile(strikes,len(spis)))
spinames =pd.DataFrame(np.repeat(["spi1","spi2","spi3","spi6"],len(strikes))) 
ratiodf = pd.DataFrame(spiratios).stack()
paymentdf = pd.DataFrame(spipayments).stack()

spidf = pd.concat([spinames,ratiodf.reset_index(drop=True), paymentdf.reset_index(drop=True),spistrikes], axis=1)
spidf.columns = ["index","ratio","payment","strike"]



allratios = noaadf.append([pdsidf,zdf,spidf,speidf])
savepath = "G:\\My Drive\\THESIS\\data\\Index Project\\Index_ratios.csv"
allratios.to_csv(savepath)


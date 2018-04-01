# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 21:12:52 2018

@author: trwi0358
"""

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


############################# Run this first ##################################
def optimalIntervalExperiment(rasterpath, targetinfo, targetarrayname, studyears, informinginfo, informingarrayname, informingyears):
    '''
        This is an experiment to check the ability of different indices to be 
            exploited for temporal trends from historic patterns.  
        
        Target arrays = payments, net payments, or anything from the indexInsurance call
        Informing arrays = payout triggers, pcfs, or anything from the indexInsurance call
    '''
    #################### Insurance Call #######################################
    # First get the insurance payment results
    ############### Argument Definitions ######################################

    if rasterpath == "d:\\data\\droughtindices\\noaa\\nad83\\raw\\":
        method = 1 # Method 1 is the present way of calculating triggers and magnitudes
        adjustit = False
        standardizeit = False
        indexit = True
    else:
        method = 2 # method 2 set strike levels based on matching probability of occurrence with the RMA index
        adjustit = True
        standardizeit = True
        indexit = False
        
    actuarialyear = 2018
    productivity = 1 
    strike = .8
    acres = 500
    allocation = .5
    difference = 0 # 0 = indemnities, 1 = net payouts, 2 = lossratios     
    maskpath = "d:\\data\\droughtindices\\masks\\nad83\\greatplains.tif"
    mask = readRaster(maskpath,1,-9999)[0]

    #run this for the PCF information period
    dfs = indexInsurance(rasterpath, actuarialyear, informingyears, informingyears, productivity, strike, 
                                 acres, allocation, adjustit = adjustit, standardizeit = standardizeit, 
                                 indexit = indexit, method = method, difference = difference,plot = False)
             
    informingarrays = dfs[informinginfo]
    ############### Find Optimal Intervals ####################################
    # Here we want to see the optimal interval choice for each cell
    # We need to find the max and second max payout, payments, or pcfs
    # First bin pcfs in monthly groups
    def optimalIntervals(arraylist):
        """
        Creates two arrays of cell-wise months associated with the highest two 
            average monthly values given an input of a monthly time series of 
            arrays. The first array is the time interval where the maximum average
            values are found, and the second array is the time interval of the 
            second highest average values. Do this with a full study period, or not
            but be careful about this.
        """
        # Groups the values into monthly averages
        months = monthlies(arraylist) # arraylist here is any of the full study period variables with names 
    
        # remove the names from the list
        justarrays = [month[1] for month in months]
    
        # Get rid of nans
        for i in justarrays:
            i[np.isnan(i)] = -9999
        
        def bestInterval(arrays):
            def bestOne(lst):
                lst = list(lst)
                ts = np.copy(lst)
                ts.sort()
                one = ts[len(ts)-1]
                p1 = lst.index(one)
                return p1
            return np.apply_along_axis(bestOne, axis = 0, arr = arrays)
    
        def secondBestInterval(arrays):
            def bestOne(lst):
                lst = list(lst)
                ts = np.copy(lst)
                ts.sort()
                two = ts[len(ts)-2]
                p2 = lst.index(two)
                return p2
            return np.apply_along_axis(bestOne, axis = 0, arr = arrays)
    
        bests = bestInterval(justarrays)*mask
        seconds = secondBestInterval(justarrays)*mask
        return [bests,seconds]
    
    # This will give the bimonthly intervals associated with the highest two pcfs
        # for each cell
    bests,seconds = optimalIntervals(informingarrays)
#    seconds = seconds*mask
    
    
    ############### Reset and Build Seasonal Payouts ##########################
    # Run again for the study years
    dfs = indexInsurance(rasterpath, actuarialyear, studyears, informingyears, productivity, strike, 
                                 acres, allocation, adjustit = adjustit, standardizeit = standardizeit, 
                                 indexit = indexit, method = method, difference = difference,plot = False) 
    targetarrays = dfs[targetinfo]
    
    # get seasonal indemnification
    winter = [i for i in targetarrays if i[0][-2:] == '11' or i[0][-2:] == '01']
    spring = [i for i in targetarrays if i[0][-2:] == '02' or i[0][-2:] == '04']
    summer = [i for i in targetarrays if i[0][-2:] == '05' or i[0][-2:] == '07']
    fall = [i for i in targetarrays if i[0][-2:] == '08' or i[0][-2:] == '10']
    
    # Get total cell-wise values
    wintersum = np.nansum([i[1] for i in winter],axis = 0)*mask
    springsum = np.nansum([i[1] for i in spring],axis = 0)*mask
    summersum = np.nansum([i[1] for i in summer],axis = 0)*mask
    fallsum = np.nansum([i[1] for i in fall],axis = 0)*mask
    
    ############### Use Optimal Intervals #####################################
    # We want a map where each cell sums up the payments from the intervals with the
        # two highest mean pcfs
    def optimalValues(arrays,yearstring,bests,seconds):
        """
        Here arrays should be a series of whichever with names, so the original 
            timeseries returns. Then we can do this for each year and add them up 
            to match the seasonal payouts. I could do all of that in a single 
            function, but that could get super confusing quickly.
        """
        # Add the best and second best arrays to the stack so that each cell's time-series 
            # includes these figures in the last two positions
        yearays = [i[1] for i in arrays if i[0][-6:-2] == yearstring]
        bests2 = np.copy(bests)
        seconds2 = np.copy(seconds)
        yearays.append(bests2)
        yearays.append(seconds2)
        
        # Remove nans, don't know how to deal with them here
        for a in yearays:
            a[np.isnan(a)] = 0
          
        # Cellwise function for each of the two intervals
        def bestOne(lst):
            lst = list(lst)        
            ts = np.copy(lst)
            bestpos = ts[len(lst)-2] # Best position is now second to last 
            values = ts[:len(lst)-2]
            top = values[int(bestpos)]
            return top
        def secondBest(lst):
            lst = list(lst)        
            ts = np.copy(lst)
            secondbestpos = ts[len(lst)-1] # and the second best is now last :)
            values = ts[:len(lst)-2]
            second = values[int(secondbestpos)]
            return second
        
        # Call each function and add the results together to simulate the optimal 
            # 50% allocation strategy based on PCFs histories.
        bestarray = np.apply_along_axis(bestOne,axis = 0, arr = yearays)*mask
        secondarray = np.apply_along_axis(secondBest, axis = 0, arr = yearays)*mask
        optimal = bestarray + secondarray
        return optimal
    
    # Now to add up the optimal payouts over the study period
    years = [str(i) for i in range(studyears[0],studyears[1]+1)]
    optimalpayments = [optimalValues(targetarrays,ys,bests,seconds) for ys in tqdm(years)]
    optimalsum = np.nansum(optimalpayments,axis = 0)*mask
    
    
    ###########################################################################
    ############################## Plot! ######################################
    ###########################################################################
    
    ############################ Shapefile ####################################
    # Main Title Business
    startyear = 2000
    endyear = 2016
    if startyear == endyear:
        endyear = ""
    else:
        endyear = ' - '+str(endyear)
    fig.suptitle(targetarrayname + '-Based Potential Payments: '+str(startyear)+str(endyear), fontsize=15,fontweight = 'bold') #+' Strike Level: %'+ str(int(strike*100))+'; Rate Year: '+str(actuarialyear)
    
    # Establish Coloring Limits
    vmin = 0
    vmax = np.nanmax(np.nanmean(optimalsum)) + .5*np.nanmax(np.nanmean(optimalsum))
    
    # Function for fromatting colorbar labels
    setCommas = FuncFormatter(lambda x, p: format(int(x), ',' ))
    
    # Establish subplot structure
    ax1 = plt.subplot2grid((3, 3), (0, 0), colspan = 1)
    ax2 = plt.subplot2grid((3, 3), (0, 1), colspan = 1)  
    ax3 = plt.subplot2grid((3, 3), (0, 2), colspan = 1)#,rowspan = 2)    
    ax4 = plt.subplot2grid((3, 3), (1, 0), colspan = 1)#,rowspan = 2) 
    ax5 = plt.subplot2grid((3, 3), (1, 1), colspan = 1)#,rowspan = 2) 
    ax6 = plt.subplot2grid((3, 3), (1, 2), colspan = 1)#,rowspan = 2) 
    
    # Set initial plot 4 parameters - this is an interactive barplot
    ax1.tick_params(which='both',right = 'off',left = 'off', bottom='off', top='off',labelleft = 'off',labelbottom='off')
    ax2.tick_params(which='both',right = 'off',left = 'off', bottom='off', top='off',labelleft = 'off',labelbottom='off')
    ax3.tick_params(which='both',right = 'off',left = 'off', bottom='off', top='off',labelleft = 'off',labelbottom='off')
    ax4.tick_params(which='both',right = 'off',left = 'off', bottom='off', top='off',labelleft = 'off',labelbottom='off')
    ax5.tick_params(which='both',right = 'off',left = 'off', bottom='off', top='off',labelleft = 'off',labelbottom='off')
    ax6.tick_params(which='both',right = 'off',left = 'off', bottom='off', top='off',labelleft = 'off',labelbottom='off')
    
    # Scootch things over
    fig.tight_layout()
    fig.subplots_adjust(left=.1, bottom=0.0, right=.975, top=.92,wspace=.015, hspace=.015)
    
    
    # Plot 1 - Payout Frequency Distribution
    im = ax1.imshow(wintersum,vmax = vmax)
    ax1.tick_params(which='both',right = 'off',left = 'off', bottom='off', top='off',labelleft = 'off',labelbottom='off') 
    ax1.set_title('Winter')
    ax1.annotate( "Intervals 11 & 1\n\n Total: $"+setCommas(np.nansum(wintersum)) + "\nMax:        $"+setCommas(np.nanmax(wintersum)),
                    xy=(.97, 0.1), xycoords='axes fraction', fontsize=6,
                    horizontalalignment='right', verticalalignment='bottom')
    
    
    # Plot 2 - Payment Calculation Factor Distribution
    im2 = ax2.imshow(springsum,vmax = vmax) 
    ax2.tick_params(which='both',right = 'off',left = 'off', bottom='off', top='off',labelleft = 'off',labelbottom='off') 
    ax2.set_title('Spring')   
    ax2.annotate( "Intervals 2 & 4\n\n Total: $"+setCommas(np.nansum(springsum)) + "\nMax:        $"+setCommas(np.nanmax(springsum)),
                    xy=(.97, 0.1), xycoords='axes fraction', fontsize=6,
                    horizontalalignment='right', verticalalignment='bottom')
    
    # Plot 3- Changes
    im3 = ax3.imshow(summersum,vmax = vmax)
    ax3.tick_params(which='both',right = 'off',left = 'off', bottom='off', top='off',labelleft = 'off',labelbottom='off') 
    ax3.set_title('Summer')
    ax3.annotate( "Intervals 5 & 7\n\n Total: $"+setCommas(np.nansum(summersum)) + "\nMax:        $"+setCommas(np.nanmax(summersum)),
                    xy=(.97, 0.1), xycoords='axes fraction', fontsize=6,
                    horizontalalignment='right', verticalalignment='bottom')
    
    # Plot 4
    im4 = ax4.imshow(fallsum,vmax = vmax)
    ax4.tick_params(which='both',right = 'off',left = 'off', bottom='off', top='off',labelleft = 'off',labelbottom='off') 
    ax4.set_title('Fall')
    ax4.annotate( "Intervals 8 & 10\n\n Total: $"+setCommas(np.nansum(fallsum)) + "\nMax:        $"+setCommas(np.nanmax(fallsum)),
                    xy=(.97, 0.1), xycoords='axes fraction', fontsize=6,
                    horizontalalignment='right', verticalalignment='bottom')
    
    # Plot 5
    im5 = ax5.imshow(optimalsum,vmax = vmax)
    ax5.tick_params(which='both',right = 'off',left = 'off', bottom='off', top='off',labelleft = 'off',labelbottom='off') 
    ax5.set_title("Highest Two "+informingarrayname+" Intervals")
    ax5.annotate( "Various Intervals\n\n Total: $"+setCommas(np.nansum(optimalsum)) + "\nMax:        $"+setCommas(np.nanmax(optimalsum)),
                    xy=(.97, 0.1), xycoords='axes fraction', fontsize=6,
                    horizontalalignment='right', verticalalignment='bottom')
    
    # Plot 6
    monthcolors = ['darkblue','b','greenyellow','yellowgreen','forestgreen',
                   'darkgreen','green','darkkhaki','saddlebrown','slategrey',
                   'cadetblue']
    
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list('mycmap', monthcolors)
    labels = ["Jan-Feb","Feb-Mar","Mar-Apr","Apr-May","May-Jun","Jun-Jul","Jul-Aug","Aug-Sep","Sep-Oct","Oct-Nov","Nov-Dec"]
    bests = bests*mask
    im6 = ax6.imshow(bests, cmap=cmap,label = labels)
    ax6.tick_params(which='both',right = 'off',left = 'off', bottom='off', top='off',labelleft = 'off',labelbottom='off') 
    ax6.set_title('Intervals With Highest ' + informingarrayname)
    legend_elements = [Patch(facecolor = monthcolors[i], label=labels[i]) for i in range(0,10)]
    ax6.legend(handles=legend_elements,loc = "right",fontsize =5.6,bbox_to_anchor=(.98, .4))
    
    # Shared Colorbar
    # add_axes order = x0, y0, width, height
    cax1 = fig.add_axes([0.075, 0.45, 0.012, 0.375]) 
    cbar = plt.colorbar(im, cax=cax1, format = setCommas)
    cbar.set_label('Potential Payment ($)', rotation=90, size = 10, labelpad =10, fontweight = 'bold')
    cbar.ax.yaxis.set_label_position('left')
    cbar.ax.yaxis.set_ticks_position('left')
    
    # Parameter info
    plt.figtext(0.45, 0.3,' Strike Level: %'+ str(int(strike*100))+'; Rate Year: '+str(actuarialyear) + '; Acres: '+str(acres),
                backgroundcolor='darkgreen',
                color='white', weight='roman', size='x-small')
    
    
    
############################## Calling here for now ############################
# For informing info and target info choose an index number for this list:
#[producerpremiums, indemnities, frequencies, pcfs, nets, lossratios, meanppremium, meanindemnity, frequencysum, meanpcf, net, lossratio]

optimalIntervalExperiment( "d:\\data\\droughtindices\\noaa\\nad83\\raw\\", 1, "Rainfall Index",[2000,2016], 2, "Payout Frequency", [1948,2016])
optimalIntervalExperiment('D:\\data\\droughtindices\\spi\\nad83\\1month\\', 1, "1-Month SPI",[2000,2016], 2, "Payout Frequency", [1948,2016])
optimalIntervalExperiment('D:\\data\\droughtindices\\spei\\nad83\\1month\\', 1,  "1-Month SPEI",[2000,2016], 2, "Payout Frequency", [1948,2016])
optimalIntervalExperiment('D:\\data\\droughtindices\\palmer\\pdsi\\nad83\\', 1, "PDSI",[2000,2016], 2, "Payout Frequency", [1948,2016])
optimalIntervalExperiment('D:\\data\\droughtindices\\palmer\\pdsisc\\nad83\\', 1, "Self Calibrated PDSI",[2000,2016], 3, "Payout Frequency", [1948,2016])

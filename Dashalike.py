# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 20:01:15 2018

@author: trwi0358
"""

# In[]:
# Import required libraries
import os
import pickle
import copy
import json
import datetime as dt
import pandas as pd
from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import xarray as xr
from plotly.graph_objs import *
import numpy as np
import plotly.plotly as py

############################ Get Payout Rasters ###############################
runfile('C:/Users/trwi0358/Github/Pasture-Rangeland-Forage/functions_git.py', wdir='C:/Users/trwi0358/Github/Pasture-Rangeland-Forage')
import warnings
warnings.filterwarnings("ignore") 
os.chdir("c:\\users\\trwi0358\\github\\pasture-rangeland-forage")
rasterpath = "d:\\data\\droughtindices\\noaa\\nad83\\raw"
source = xr.open_rasterio("d:\\data\\droughtindices\\rma\\nad83\\prfgrid.tif")
grid = readRaster('data\\rma\\nad83\\prfgrid.tif',1,-9999)[0]

#rasterpath = "f:\\data\\droughtindices\\noaa\\"+proj+"\\raw"
method = 2 # Method 1 is the present way of calculating triggers and magnitudes
adjustit = True
actuarialyear = 2018
standardizeit = True
indexit = False
productivity = 1 
strike = .7
acres = 500
allocation = .5
difference = 0 # 0 = indemnities, 1 = net payouts, 2 = lossratios 
studyears = [2000,2017]
baselineyears = [1948, 2016]
return_type = 5
###############################################################################
############################ Create the App Object ############################
###############################################################################
# Create Dash Application Object
app = dash.Dash(__name__)
# I really need to get my own stylesheet, if anyone know how to do this...
app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501
# Create server object
server = app.server
# No idea
CORS(server)
# Create and initialize a cache for storing data - data pocket
cache = Cache(config = {'CACHE_TYPE':'simple'})
cache.init_app(server)

###############################################################################
############################ Create Lists and Dictionaries ####################
###############################################################################
# Index Paths
indices = [{'label':'PDSI','value':'D:\\data\\droughtindices\\palmer\\pdsi\\nad83\\'},
          {'label':'PDSI-Self Calibrated','value':'D:\\data\\droughtindices\\palmer\\pdsisc\\nad83\\'},
          {'label':'Palmer Z Index','value':'D:\\data\\droughtindices\\palmer\\pdsiz\\nad83\\'},
          {'label':'EDDI-1','value':'D:\\data\\droughtindices\\eddi\\nad83\\monthly\\1month\\'},
          {'label':'EDDI-2','value': 'D:\\data\\droughtindices\\eddi\\nad83\\monthly\\2month\\'},
          {'label':'EDDI-3','value':'D:\\data\\droughtindices\\eddi\\nad83\\monthly\\3month\\'},
          {'label':'EDDI-6','value':'D:\\data\\droughtindices\\eddi\\nad83\\monthly\\6month\\'},
          {'label':'SPI-1' ,'value': 'D:\\data\\droughtindices\\spi\\nad83\\1month\\'},
          {'label':'SPI-2' ,'value': 'D:\\data\\droughtindices\\spi\\nad83\\2month\\'},
          {'label':'SPI-3' ,'value': 'D:\\data\\droughtindices\\spi\\nad83\\3month\\'},
          {'label':'SPI-6' ,'value': 'D:\\data\\droughtindices\\spi\\nad83\\6month\\'},
          {'label':'SPEI-1' ,'value': 'D:\\data\\droughtindices\\spei\\nad83\\1month\\'},
          {'label':'SPEI-2' ,'value': 'D:\\data\\droughtindices\\spei\\nad83\\2month\\'},
          {'label':'SPEI-3' ,'value': 'D:\\data\\droughtindices\\spei\\nad83\\3month\\'},
          {'label':'SPEI-6','value': 'D:\\data\\droughtindices\\spei\\nad83\\6month\\'}]
# Index names, using the paths we already have. These are for titles.
indexnames = {'D:\\data\\droughtindices\\palmer\\pdsi\\nad83\\': 'Palmer Drought Severity Index',
          'D:\\data\\droughtindices\\palmer\\pdsisc\\nad83\\': 'Self-Calibrated Palmer Drought Severity Index',
          'D:\\data\\droughtindices\\palmer\\pdsiz\\nad83\\': 'Palmer Z Index',
          'D:\\data\\droughtindices\\eddi\\nad83\\monthly\\1month\\':'Evaporative Demand Drought Index - 1 month',
          'D:\\data\\droughtindices\\eddi\\nad83\\monthly\\2month\\':'Evaporative Demand Drought Index - 2 month',
          'D:\\data\\droughtindices\\eddi\\nad83\\monthly\\3month\\':'Evaporative Demand Drought Index - 3 month',
          'D:\\data\\droughtindices\\eddi\\nad83\\monthly\\6month\\':'Evaporative Demand Drought Index - 6 month',
          'D:\\data\\droughtindices\\spi\\nad83\\1month\\':'Standardized Precipitation Index - 1 month',
          'D:\\data\\droughtindices\\spi\\nad83\\2month\\':'Standardized Precipitation Index - 2 month',
          'D:\\data\\droughtindices\\spi\\nad83\\3month\\':'Standardized Precipitation Index - 3 month',
          'D:\\data\\droughtindices\\spi\\nad83\\6month\\':'Standardized Precipitation Index - 6 month',
          'D:\\data\\droughtindices\\spei\\nad83\\1month\\': 'Standardized Precipitation-Evapotranspiration Index - 1 month', 
          'D:\\data\\droughtindices\\spei\\nad83\\2month\\': 'Standardized Precipitation-Evapotranspiration Index - 2 month', 
          'D:\\data\\droughtindices\\spei\\nad83\\3month\\': 'Standardized Precipitation-Evapotranspiration Index - 3 month', 
          'D:\\data\\droughtindices\\spei\\nad83\\6month\\': 'Standardized Precipitation-Evapotranspiration Index - 6 month'}

# The indexInsurance function returns many items. The order is:
    # producerpremiums,indemnities,frequencies,pcfs,meanppremium,meanindemnity,frequencysum,meanpcf
# This is for accessing the dataset
returns = [{'label':'Potential Producer Premiums','value':'4'},
          {'label':'Potential Indemnities','value':'5'},
          {'label':'Potential Payout Frequencies','value':'6'},
          {'label':'Potential Payment Calculation Factors','value':'7'}]
# The next two are for labels and titles
returnames = {4:'Potential Producer Premiums',
              5:'Potential Indemnities',
              6:'Potential Payout Frequencies',
              7:'Potential Payment Calculation Factors'}
returnabbrvs = {4:'P.P.',
                5:'P.I.',
                6:'P.F.',
                7:'P.C.F.'}

# Strike levels
strikes = [{'label':'70%','value':.70},
          {'label':'75%','value':.75},
          {'label':'80%','value':.80},
          {'label':'85%','value':.85},
          {'label':'90%','value':.90}]

# Create Coordinate Index - because I can't find the array position in the 
    # click event!
xs = range(300)
ys = range(120)
lons = [-129.75 + .25*x for x in range(0,300)]
lats = [49.75 - .25*x for x in range(0,120)]
londict = dict(zip(lons, xs))
latdict = dict(zip(lats,ys))

# Create global chart template
mapbox_access_token = 'pk.eyJ1IjoidHJhdmlzc2l1cyIsImEiOiJjamVrc2duZXE0OWNxMndxZTJ1c3g0cDByIn0.XrtTRpRzjw0f-arNCiTpoA'

# Map Layout:
layout = dict(
    autosize=True,
    height=500,
    font=dict(color='#CCCCCC'),
    titlefont=dict(color='#CCCCCC', size='20'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=65
    ),
    hovermode="closest",
    plot_bgcolor="#191A1A",
    paper_bgcolor="#020202",
    legend=dict(font=dict(size=10), orientation='h'),
    title='Potential Payout Frequencies',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="dark",
        center=dict(
            lon= -95.7,
            lat= 37.1
        ),
        zoom=3,
    )
)


# In[]:
# Create app layout
app.layout = html.Div(
    [
        html.Div(# One
            [
                html.H1(
                    'Pasture Rangeland and Forage',
                    className='eight columns',
                ),
                html.Img(
                    src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe.png",
                    className='one columns',
                    style={
                        'height': '100',
                        'width': '225',
                        'float': 'right',
                        'position': 'relative',
                    },
                ),
            ],
            className='row'
        ),
        html.Div(# Two
            [
                html.H5(
                    '',
                    id='year_text',
                    className='two columns',
                    style={'text-align': 'center'}
                ),

                html.H5(
                    '',
                    id='year_text2',
                    className='two columns',
                    style={'text-align': 'center'}
                ),                
            ],
            className='row'
        ),
        html.Div(
            [
                html.P('Study Period Year Range'),  
                dcc.RangeSlider(
                    id='year_slider',
                    min=1948,
                    max=2017,
                    value=[2000, 2017]
                ),
                html.P('Baseline Average Year Range'), 
                dcc.RangeSlider(
                    id='year_slider2',
                    min=1948,
                    max=2017,
                    value=[1948, 2016]
                ),
            ],
            style={'margin-top': '20'}
        ),
        html.Div(# Four
            [
                html.Div(# Four-a
                    [
                        html.P('Drought Index'),
                        dcc.Dropdown(
                            id='index_choice',
                            options=indices,
                            multi=False,
                            value=[]#'D:\\data\\droughtindices\\palmer\\pdsi\\nad83\\'
                        ),
                        html.P('Choose Information Type'),
                        dcc.Dropdown(
                            id='return_type',
                            options=returns,
                            multi=False,
                            value='5'
                        ),
                    ],
                    className='six columns'
                ),
                html.Div(# Four-a
                    [
                        html.P('Gaurantee Level'),
                        dcc.RadioItems(
                            id='strike_level',
                            options=strikes,
                            value=.75,
                            labelStyle={'display': 'inline-block'}
                        ),                        
                        html.P('Actuarial Year'),
                        dcc.RadioItems(
                            id='actuarial_year',
                            options=[{'label':'2017','value':2017},
                                      {'label':'2018','value':2018}],
                            value=2018,
                            labelStyle={'display': 'inline-block'}
                        ),
                        html.P('Number of Acres'),
                        dcc.Input(
                            id = 'acres',
                            placeholder='Number of acres...',
                            type='number',
                            value=500
                        )
                    ],
                    className='six columns'
                ),
               ],
                className = 'row'
            ),
        html.Div(#Five
            [
                html.Div(#Five-a
                    [
                        dcc.Graph(id='main_graph')
                    ],
                    className='eight columns',
                    style={'margin-top': '20'}
                ),
                html.Div(# Five-b
                    [
                        dcc.Graph(id='trend_graph')
                    ],
                    className='four columns',
                    style={'margin-top': '20'}
                ),
            ],
            className='row'
        ),
        html.Div(#Six
            [
                html.Div(#Six-a
                    [
                        dcc.Graph(id='series_graph')
                    ],
                    className='four columns',
                    style={'margin-top': '10'}
                ),
                html.Div(#Six-a
                    [
                        dcc.Graph(id='histogram')
                    ],
                    className='four columns',
                    style={'margin-top': '10'}
                ),


            ],
            className='row'
        ),
        html.Div(id='signal', style={'display': 'none'})
    ],
    className='ten columns offset-by-one'
)


# In[]:
############################################################################### 
######################### Create Cache ######################################## 
############################################################################### 
@cache.memoize()
def global_store(signal):
    # Transform the argument list back to normal
    signal = json.loads(signal)
    
    # Get the new insurance arrays with the mondo function. 
    df = indexInsurance(signal[0], signal[1], signal[2], 
                             signal[3], productivity, signal[4],signal[5], allocation, 
                             adjustit = adjustit,standardizeit = standardizeit, 
                             indexit = indexit, method = method, difference = difference)
    return df
        
def retrieve_data(signal):
    df = global_store(signal)
    return df

# Store the data in the cache and hide the signal to activate it in the hidden div
@app.callback(Output('signal', 'children'), 
              [Input('index_choice', 'value'),
               Input('actuarial_year','value'),
               Input('year_slider','value'),
               Input('year_slider2','value'),
               Input('strike_level','value'),
               Input('acres','value')])
def compute_value(index_choice,actuarial_year,year_slider,year_slider2,strike_level,acres):
    signal = json.dumps([index_choice,actuarial_year,year_slider,year_slider2,strike_level,acres])
    # compute value and send a signal when done
    global_store(signal)
    return signal
############################################################################### 
######################### Create Callbacks #################################### 
############################################################################### 
# Other Call Backs
 # Slider1 -> Base line Year text
@app.callback(Output('year_text', 'children'),
              [Input('year_slider', 'value')])
def update_year_text(year_slider):
    return "Study Period: {} | {} ".format(year_slider[0], year_slider[1])

# Slider2 -> Study Year text
@app.callback(Output('year_text2', 'children'),
              [Input('year_slider2', 'value')])
def update_year_text2(year_slider2):
    return "Baseline: " + str(year_slider2[0]) + " | " + str(year_slider2[1])

###############################################################################
######################### Graph Builders ######################################
###############################################################################
@app.callback(Output('main_graph', 'figure'),
              [Input('signal','children'),
               Input('return_type','value'),
               Input('strike_level','value')])   
def changeIndex(signal,return_type,strike_level):
    """
    This will be the map itself, it is not just for changing maps.
        In order to map over mapbox we are creating a scattermapbox object.
    """
    
    # Choose the mean pcf map from above
    # insurance_package_all = [producerpremiums,indemnities,frequencies,pcfs,meanppremium,meanindemnity,frequencysum,meanpcf]
    df = retrieve_data(signal)
    data = df[5]
    signal = json.loads(signal)
    # Second, convert data back into an array, but in a from xarray recognizes
    array = np.array([data],dtype = "float32")
    
    # Third, change the source array to this one. Source is defined up top
    source.data = array
    
    # Fourth, bin the values into lat, long points for the dataframe
    dfs = xr.DataArray(source, name = "data")
    pdf = dfs.to_dataframe()
    step = .25
    to_bin = lambda x: np.floor(x / step) * step
    pdf["latbin"] = pdf.index.get_level_values('y').map(to_bin)
    pdf["lonbin"] = pdf.index.get_level_values('x').map(to_bin)
    groups = pdf.groupby(("latbin", "lonbin"))
    df_flat = pdf.drop_duplicates(subset=['latbin', 'lonbin'])
    df= df_flat[np.isfinite(df_flat['data'])]
    colorscale = [[0, 'rgb(54, 50, 153)'], [0.35, 'rgb(17, 123, 215)'],
                    [0.5, 'rgb(37, 180, 167)'], [0.6, 'rgb(134, 191, 118)'],
                    [0.7, 'rgb(249, 210, 41)'], [1.0, 'rgb(244, 236, 21)']]

# Create the scattermapbox object
    data = [ dict(
        type = 'scattermapbox',
#        locationmode = 'USA-states',
        lon = df['lonbin'],
        lat = df['latbin'],
        text =df['data'],
        mode = 'markers',
        marker = dict(
            colorscale = colorscale,
            cmin = 0,
            color = df['data'],
            cmax = df['data'].max(),
            opacity=0.85,
            colorbar=dict(  
                title=returnabbrvs.get(int(return_type)),
                textposition = "auto",
                orientation = "h"
            )
        ))]
     

    # Title Business
    if return_type == 6:
        calc = "Sum "
    else:
        calc = "Average "
    layout['title'] = indexnames.get(signal[0]) +"<br>"+calc+returnames.get(int(return_type))+"  |  " +str(signal[2][0]) + " to " + str(signal[2][1])+ "  |  " + str(int(strike_level*100)) + "% Strike Level"
               
    # Seventh wrap the data and layout into one
    figure = dict(data=data, layout=layout)
#    return {'figure':figure,'info': index_package_all}
    return figure

###############################################################################
###############################################################################
###############################################################################
@app.callback(Output('trend_graph','figure'),
               [Input('main_graph','clickData'),
                Input('signal','children'),
                Input('return_type','value')])
def makeTrendBar(clickData,signal,return_type):
    if clickData is None:
        return {}
#        opacity = 1
#    
    # Get data
    df = retrieve_data(signal)
    
    # Adjust the index position for the time series form of the chosen information
    indx = int(return_type) - 4
    
    # if return_type = frequencies (6) - use the summation array

    # get series of pcfs
    series = df[indx]
    
    # Get the array positions
    x = londict.get(clickData['points'][0]['lon'])
    y = latdict.get(clickData['points'][0]['lat'])
    
    # Catch the target grid cell
    targetid  = grid[y,x]
    index = np.where(grid == targetid)
    
    # Create the time series of data at that gridcell
    timeseries = [[item[0],item[1][index]] for item in series]
    
    # For title
    years = [int(item[0][-6:-2]) for item in timeseries]
    year1 = str(min(years)) 
    year2 = str(max(years))
    
    # For the x axis and value matching
    intervals = [format(int(interval),'02d') for interval in range(1,12)]
    months = {1:'Jan-Feb',
              2:'Feb-Mar',
              3:'Mar-Apr',
              4:'Apr-May',
              5:'May-Jun',
              6:'Jun-Jul',
              7:'Jul-Aug',
              8:'Aug-Sep',
              9:'Sep-Oct',
              10:'Oct-Nov',
              11:'Nov-Dec'}
    
    # The actual values
    valuelist = [[series[1] for series in timeseries if series[0][-2:] ==  interval] for interval in intervals]
    
    # In tuple form for the bar chart
    # if return_type = frequencies (6) - use the summation instead of mean
    if int(return_type) == 6:
        averages =  tuple(np.asarray([np.sum(sublist) for sublist in valuelist]))
        calc = "Sums "
    else:
        averages =  tuple(np.asarray([np.mean(sublist) for sublist in valuelist]))
        calc = "Averages "
        
    intlabels = [months.get(i) for i in range(1,12)]
    x = np.arange(len(intervals))    
    
    layout_count = copy.deepcopy(layout)

    data = [
        dict(
            type='scatter',
            mode='markers',
            x=x,
            y=averages,
            name= returnabbrvs.get(int(return_type)),
            opacity=0,
            hoverinfo='skip'
        ),
        dict(
            type='bar',
            x=x,
            y=averages,
        ),
    ]
    
    
    layout_count['title'] = returnabbrvs.get(int(return_type))+ ' Monthly Trends: '+calc + '<br> Grid ID: '+ str(int(targetid))
    layout_count['dragmode'] = 'select'
    layout_count['showlegend'] = False
    layout_count['xaxis'] = dict(tickvals = x, ticktext = intlabels)

    figure = dict(data=data, layout=layout_count)
    return figure
###############################################################################
###############################################################################
###############################################################################
@app.callback(Output('series_graph','figure'),
               [Input('main_graph','clickData'),
                Input('signal','children'),
                Input('return_type','value')])
def makeSeries(clickData,signal,return_type):
    if clickData is None:
        return {}
    
    # Get data
    df = retrieve_data(signal)
    # Adjust the index position for the time series form of the chosen information
    indx = int(return_type) - 4
    
    series = df[indx]
    
    # Get the array positions
    x = londict.get(clickData['points'][0]['lon'])
    y = latdict.get(clickData['points'][0]['lat'])
    
    # Catch the target grid cell
    targetid  = grid[y,x]
    index = np.where(grid == targetid)
    
    # Create the time series of data at that gridcell
    values = [float(item[1][index]) for item in series]
    

    # For title
    years = [item[0][-6:-2]+"/"+ item[0][-2:] for item in series]
    year1 = str(min(years)) 
    year2 = str(max(years))
        
    # For yearly frequency sums
    if int(return_type) == 6:
        years = np.unique([item[0][-6:-2] for item in series])
        values = [np.sum([item[1][index] for item in series if item[0][-6:-2] == y]) for y in years] 
    layout_count = copy.deepcopy(layout)

    data = [
        dict(
            type='scatter',
            mode='lines+markers',
            name= returnames.get(int(return_type)),
            x = years,
            y = values,
            line=dict(
                    shape="spline",
                    smoothing=2,
                    width=3,
                    color='#228B22'
            ),
            marker=dict(symbol='diamond-open')
        ),
    ]
        
    layout_count['title'] =  returnabbrvs.get(int(return_type))+' Time Series <br> Grid ID: ' + str(int(targetid))
    layout_count['dragmode'] = 'select'
    layout_count['showlegend'] = False
    figure = dict(data=data, layout=layout_count)
    
    return figure
###############################################################################
###############################################################################
###############################################################################
@app.callback(Output('histogram','figure'),
               [Input('signal','children'),
                Input('return_type','value')])
def makeHist(signal,return_type):
    # Get data
    df = retrieve_data(signal)
    
    # Adjust the index position for the time series form of the chosen information    
    # if return_type = frequencies (6) - use the summation array
    if int(return_type) == 6:
        indx = int(return_type)
    else:
        indx = int(return_type) - 4

    # Extract dataset
    series = df[indx]
    
    
    # Make Adjustments for different infromation returns
    if int(return_type) == 6:
        values = series
        uniques = np.unique(values)
        uniques = [v for v in uniques if np.isfinite(v)]
        bins = len(uniques)
        scalar = 0

    elif int(return_type) == 5:
        values = [item[1] for item in series]
        bins = 100
        scalar = .1
        
    else:
        values = [item[1] for item in series]
        bins = 100
        scalar = 0

    
    # Build bins
    amax = np.nanmax(values)
    amin = np.nanmin(values)
    hists,bins = np.histogram(values,range = [amin + scalar,amax],bins = bins)
    hists = tuple(hists)
    bins = list(bins)
    layout_count = copy.deepcopy(layout)

    data = [
        dict(
            type='scatter',
            mode='markers',
            x=bins,
            y=hists,
            name= returnabbrvs.get(int(return_type))+' Value Ditribution',
            opacity=0,
            hoverinfo='skip'
        ),
        dict(
            type='bar',
            x=bins,
            y=hists,
            marker = dict(
                    color = '#ADD8E6'
            ),
        ),
    ]
    layout_count['title'] = returnames.get(int(return_type))+ ' Value Distribution'
    layout_count['dragmode'] = 'select'
    layout_count['showlegend'] = False
#    layout_count['xaxis'] = dict(tickvals = x, ticktext = intlabels)

    figure = dict(data=data, layout=layout_count)
    return figure

# In[]:
# Main
if __name__ == '__main__':
    app.server.run(use_reloader = False)#debug=True, threaded=True

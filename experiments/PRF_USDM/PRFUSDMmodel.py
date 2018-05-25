# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 23:00:32 2018

Basis Risk of PRF payouts by conditional probability with the USDM


The plan here is to take the weekly US Drought Monitor rasters and convert them
    into bi-monthyl values. I think I may use the weekly mode to start. 
    Then I will take the bi-monthly RMA and calculate the number of times each
    cell recieves no payout when the drought monitor indicates drought of a 
    severity comparable to the strike level in the RMA
    
Things to do:
    1) Place the Rainfall index payout triggers next to USDM DM categories
    2) Put a tooltip to each graph
    3) Run each parameter and store in s3 bucket
    4) Consider a graph for each location
    5) Weight ratio by number of PRF payout triggers
        i) Because a signular miss does not tell us much...
        ii) Perhaps simply multiply each ratio by the number of triggers and then
            standardize?
    6) Get a nation-wide figure that sums up the "basis risk" according to the USDM
        i) average ratio (USDM pay: NOAA pay)?

@author: trwi0358
"""


# In[]:
# Import required libraries
############################ Get Functions ####################################
runfile('C:/Users/trwi0358/Github/Pasture-Rangeland-Forage/functions_git.py', wdir='C:/Users/trwi0358/Github/Pasture-Rangeland-Forage')
############################ Get Payout Rasters ###############################
import warnings
warnings.filterwarnings("ignore") 
os.chdir("c:\\users\\trwi0358\\github\\pasture-rangeland-forage")
source = xr.open_rasterio("d:\\data\\droughtindices\\rma\\nad83\\prfgrid.tif")
source_signal = '["D:\\\\data\\\\droughtindices\\\\noaa\\\\nad83\\\\indexvalues\\\\", 4, 0.7]'
grid = readRaster('data\\rma\\nad83\\prfgrid.tif',1,-9999)[0]
strike = .7
mask = readRaster('D:\\data\\droughtindices\\masks\\nad83\\mask4.tif',1,-9999)[0]
# Load pre-conditioned bi-monthly USDM modal category rasters into numpy arrays
usdmodes = readRasters("D:\\data\\droughtindices\\usdm\\usdmrasters\\nad83\\usdmeans\\",-9999)[0]

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
indices = [{'label':'RMA','value':'D:\\data\\droughtindices\\noaa\\nad83\\indexvalues\\'},
           {'label':'PDSI','value':'D:\\data\\droughtindices\\palmer\\pdsi\\nad83\\'},
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
indexnames = {'D:\\data\\droughtindices\\noaa\\nad83\\indexvalues\\': 'Risk Management Agency Rainfall Index',
            'D:\\data\\droughtindices\\palmer\\pdsi\\nad83\\': 'Palmer Drought Severity Index',
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

# Strike levels
strikes = [{'label':'70%','value':.70},
          {'label':'75%','value':.75},
          {'label':'80%','value':.80},
          {'label':'85%','value':.85},
          {'label':'90%','value':.90}]

DMs = [{'label':'D4','value':4},
       {'label':'D3','value':3},
       {'label':'D2','value':2},
       {'label':'D1','value':1},
       {'label':'D0','value':0}]
       
          
DMlabels = {0:'D0',
          1:'D1',
          2:'D2',
          3:'D3',
          4:'D4'}
# Create Coordinate Index - because I can't find the array position in the 
    # click event!
xs = range(300)
ys = range(120)
lons = [-129.75 + .25*x for x in range(0,300)]
lats = [49.75 - .25*x for x in range(0,120)]
londict = dict(zip(lons, xs))
latdict = dict(zip(lats,ys))


# Create global chart template
mapbox_access_token = 'pk.eyJ1IjoidHJhdmlzc2l1cyIsImEiOiJjamZiaHh4b28waXNkMnptaWlwcHZvdzdoIn0.9pxpgXxyyhM6qEF_dcyjIQ'

# Map Layout:
layout = dict(
    autosize=True,
    height=500,
    font=dict(color='#CCCCCC'),
    titlefont=dict(color='#CCCCCC', size='20'),
    margin=dict(
        l=10,
        r=10,
        b=35,
        t=55
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
                    'Pasture Rangeland and Forage - USDM Basis Risk Check',
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
        html.Div(# Four
            [
                html.Div(# Four-a
                    [
                        html.P('Drought Index'),
                        dcc.Dropdown(
                            id = 'index_choice',
                            options = indices,
                            multi = False,
                            value = "D:\\data\\droughtindices\\noaa\\nad83\\raw\\"#'D:\\data\\droughtindices\\palmer\\pdsi\\nad83\\'
                        ),
                    ],
                    className='six columns'
                ),
                html.Div(# Four-a
                    [
                        html.P('RMA Strike Level'),
                        dcc.RadioItems(
                            id='strike_level',
                            options=strikes,
                            value=.75,
                            labelStyle={'display': 'inline-block'}
                        ),                        
                        html.P('USDM Category'),
                        dcc.RadioItems(
                            id='usdm_level',
                            options=DMs,
                            value=4,
                            labelStyle={'display': 'inline-block'}
                        ),
                    ],
                    className='six columns'
                ),
               ],
                className = 'row'
            ),
        html.Div(#Six
            [
                html.Div(#Six-a
                    [
                        dcc.Graph(id='main_graph')
                    ],
                    className='eight columns',
                    style={'margin-top': '10'}
                ),
                html.Div(#Six-a
                    [
                        dcc.Graph(id='drought_graph')
                    ],
                    className='four columns',
                    style={'margin-top': '10'}
                ),
#                
            ],
            className='row'
        ),
                
        html.Div(#Six
            [
                html.Div(#Six-a
                    [
                        dcc.Graph(id='hit_graph')
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
    if not signal:
        signal = source_signal
    signal = json.loads(signal)
    
    # Unpack signals
    index_choice = signal[0]
    usdm_level = signal[1]
    strike_level = signal[2]
   
    # Get the index to compare to usdm
    indexlist, geom, proj = readRasters2(index_choice,-9999)

    # Now, to check both against each other, but first, match times
    udates = [m[0][-6:] for m in usdmodes]
    indexlist = [i for i in indexlist if i[0][-6:] in udates]
    idates = [m[0][-6:] for m in indexlist]
    usdms = [u for u in usdmodes if u[0][-6:] in idates]
    
    # Create a list of monthly arrays with 1's for the scenario
    risks = [basisCheck(usdm = usdms[i],noaa = indexlist[i],strike = strike_level, dm = usdm_level) for i in range(len(usdms))]
    
    # Sum them up
    hits = np.nansum(risks,axis = 0)*mask
#    hits[hits==0]  = .01

    # Create a list of monthly arrays with 1's for droughts
    droughts = [droughtCheck(usdm = usdmodes[i],dm = usdm_level) for i in range(len(usdmodes))]
#    droughtchances[droughtchances == 0] = 1000

    # Sum and divide by time steps
    droughtchances = np.nansum(droughts,axis = 0)*mask
    
    # Final Basis risk according to the USDM and Muneepeerakul et als method
    basisrisk = hits/droughtchances
    
    # Package Returns for later
    df = [basisrisk, droughtchances,hits]
    
    return df
        
def retrieve_data(signal):
    df = global_store(signal)
    return df

# Store the data in the cache and hide the signal to activate it in the hidden div
@app.callback(Output('signal', 'children'), 
              [Input('index_choice','value'),
               Input('usdm_level','value'),
               Input('strike_level','value')])
def compute_value(index_choice,usdm_level,strike_level):
    # Package the function arguments
    signal = json.dumps([index_choice,usdm_level,strike_level])
    
    # compute value and send a signal when done
    global_store(signal)
    return signal

############################################################################### 
######################### Create Callbacks #################################### 
############################################################################### 

###############################################################################
######################### Graph Builders ######################################
###############################################################################
@app.callback(Output('main_graph', 'figure'),
              [Input('signal','children')])
def basisGraph(signal):
    """
    This will be the drought occurrence map, in order to map over mapbox we are
        creating a scattermapbox object.
    """     
    
    # Get data
    df = retrieve_data(signal)
    
    # Transform the argument list back to normal 
    if not signal:
        signal= source_signal
    signal = json.loads(signal)
    
    # Unpack signals
    index_choice = signal[0]
    usdm_level = signal[1]
    strike_level = signal[2]
    
    
    # Get desired array
    droughtchances = df[0]
    
    # Second, convert data back into an array, but in a form xarray recognizes
    array = np.array([droughtchances],dtype = "float32")
    
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
    
    # Add Grid IDs
    colorscale = [[0, 'rgb(2, 0, 68)'], [0.35, 'rgb(17, 123, 215)'],# Make darker (pretty sure this one)
                    [0.45, 'rgb(37, 180, 167)'], [0.55, 'rgb(134, 191, 118)'],
                    [0.7, 'rgb(249, 210, 41)'], [1.0, 'rgb(255, 249, 0)']] # Make darker
    
# Create the scattermapbox object
    data = [ 
        dict(
        type = 'scattermapbox',
#        locationmode = 'USA-states',
        lon = df['lonbin'],
        lat = df['latbin'],
        text = np.round(df['data'],2),
        mode = 'markers',
        marker = dict(
            colorscale = colorscale,
            cmin = 0,
            color = df['data'],
            cmax = df['data'].max(),
            opacity=0.85,
            colorbar=dict(  
                title= "BR",
                textposition = "auto",
                orientation = "h"
                )
            )
        )]
            
    layout['title'] = indexnames.get(index_choice) + " Risk According to <br>" + DMlabels.get(usdm_level) +" USDM Severity"
               
    # Seventh wrap the data and layout into one
    figure = dict(data=data, layout=layout)
#    return {'figure':figure,'info': index_package_all}
    return figure




@app.callback(Output('drought_graph', 'figure'),
              [Input('signal','children')])
def droughtGraph(signal):
    """
    This will be the drought occurrence map, in order to map over mapbox we are
        creating a scattermapbox object.
    """     
    
    # Get data
    df = retrieve_data(signal)
    
    # Transform the argument list back to normal    
    signal = json.loads(signal)
    
    # Unpack signals
    index_choice = signal[0]
    usdm_level = signal[1]
    strike_level = signal[2]
    
    
    # Get desired array
    droughtchances = df[1]
    
    # Second, convert data back into an array, but in a from xarray recognizes
    array = np.array([droughtchances],dtype = "float32")
    
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
    
    # Add Grid IDs
    colorscale = [[0, 'rgb(2, 0, 68)'], [0.35, 'rgb(17, 123, 215)'],# Make darker (pretty sure this one)
                    [0.45, 'rgb(37, 180, 167)'], [0.55, 'rgb(134, 191, 118)'],
                    [0.7, 'rgb(249, 210, 41)'], [1.0, 'rgb(255, 249, 0)']] # Make darker
    
# Create the scattermapbox object
    data = [ 
        dict(
        type = 'scattermapbox',
#        locationmode = 'USA-states',
        lon = df['lonbin'],
        lat = df['latbin'],
        text = np.round(df['data'],2),
        mode = 'markers',
        marker = dict(
            colorscale = colorscale,
            cmin = 0,
            color = df['data'],
            cmax = df['data'].max(),
            opacity=0.85,
            colorbar=dict(  
                title= "Frequency",
                textposition = "auto",
                orientation = "h"
                )
            )
        )]
            
    layout['title'] = "USDM Category " + DMlabels.get(usdm_level) +" Frequency"
    layout['mapbox']['zoom'] = 2 
    
    # Seventh wrap the data and layout into one
    figure = dict(data=data, layout=layout)
#    return {'figure':figure,'info': index_package_all}
    return figure




@app.callback(Output('hit_graph', 'figure'),
              [Input('signal','children')])
def droughtGraph(signal):
    """
    This will be the drought occurrence map, in order to map over mapbox we are
        creating a scattermapbox object.
    """     
    
    # Get data
    df = retrieve_data(signal)
    
    # Transform the argument list back to normal    
    signal = json.loads(signal)
    
    # Unpack signals
    index_choice = signal[0]
    usdm_level = signal[1]
    strike_level = signal[2]
    
    
    # Get desired array
    droughtchances = df[2]
    
    # Second, convert data back into an array, but in a from xarray recognizes
    array = np.array([droughtchances],dtype = "float32")
    
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
    
    # Add Grid IDs
    colorscale = [[0, 'rgb(2, 0, 68)'], [0.35, 'rgb(17, 123, 215)'],# Make darker (pretty sure this one)
                    [0.45, 'rgb(37, 180, 167)'], [0.55, 'rgb(134, 191, 118)'],
                    [0.7, 'rgb(249, 210, 41)'], [1.0, 'rgb(255, 249, 0)']] # Make darker
    
# Create the scattermapbox object
    data = [ 
        dict(
        type = 'scattermapbox',
#        locationmode = 'USA-states',
        lon = df['lonbin'],
        lat = df['latbin'],
        text = np.round(df['data'],2),
        mode = 'markers',
        marker = dict(
            colorscale = colorscale,
            cmin = 0,
            color = df['data'],
            cmax = df['data'].max(),
            opacity=0.85,
            colorbar=dict(  
                title= "Frequency",
                textposition = "auto",
                orientation = "h"
                )
            )
        )]
            
    layout['title'] = indexnames.get(index_choice) + "<br> Didn't Pay | USDM Indicated Drought"
    layout['mapbox']['zoom'] = 2
    # Seventh wrap the data and layout into one
    figure = dict(data=data, layout=layout)
#    return {'figure':figure,'info': index_package_all}
    return figure
# In[]:
# Main
if __name__ == '__main__':
    app.server.run(use_reloader = False)#debug=True, threaded=True




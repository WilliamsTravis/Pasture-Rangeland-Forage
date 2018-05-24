# -*- coding: utf-8 -*-
"""
Update to the Time series:
    5) Use this as an example to push to the internet
        a) How to access source files directly from git hub?
        b) Use these guides for pushing to heroku
            i) https://dash.plot.ly/deployment
            ii) https://www.youtube.com/watch?v=tpn-5qPnrrc

Created on Mon May 21 10:32:24 2018

@author: trwi0358
"""

# In[]:
############################ Get Functions ####################################
runfile('C:/Users/trwi0358/Github/Pasture-Rangeland-Forage/functions_git.py',
        wdir='C:/Users/trwi0358/Github/Pasture-Rangeland-Forage') # Change to github

################# Test with Local Drive or Online with AWS files? #############
test = True

# In[]:
####################################################################################################
############################ Create the App Object #################################################
####################################################################################################
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

# In[]:
############################ Set up initial Signal #################################################
import warnings
import io
warnings.filterwarnings("ignore") 
os.chdir("c:\\users\\trwi0358\\github\\pasture-rangeland-forage") # Change to github
rasterpath = "d:\\data\\droughtindices\\noaa\\nad83\\raw\\" # Change to github
source = xr.open_rasterio("d:\\data\\droughtindices\\rma\\nad83\\prfgrid.tif") # Change to github
source_signal = '["noaa", 2018, [2000, 2017], 0.7, "indemnities"]'
grid = readRaster('data\\rma\\nad83\\prfgrid.tif',1,-9999)[0]
datatable = pd.read_csv("C:\\Users\\trwi0358\\Github\\Pasture-Rangeland-Forage\\data\\PRFIndex_specs.csv").to_dict('RECORDS')
productivity = 1


# In[]: 
####################################################################################################
############################# Create AWS bucket ####################################################
####################################################################################################
# If you want to use urls
#session = boto3.session.Session(region_name='us-west-2')
#s3client = session.client('s3', config= boto3.session.Config(signature_version='s3v4'),
#                          aws_access_key_id='my-ACCESS-KEY-ID',
#                          aws_secret_access_key='my-ACCESS-KEY')

client = boto3.client('s3') #low-level functional API
resource = boto3.resource('s3') #high-level object-oriented API
bucket = resource.Bucket('pasture-rangeland-forage') 

# In[]:
###############################################################################
############################ Create Lists and Dictionaries ####################
###############################################################################
# Index Paths
# Index names, using the paths we already have. These are for titles.
indices = [{'label':'NOAA','value':'noaa'},
           {'label':'PDSI','value':'pdsi'},
           {'label':'PDSI-Self Calibrated','value':'pdsisc'},
           {'label':'Palmer Z Index','value':'pdsiz'},
           {'label':'SPI-1' ,'value': 'spi1'},
           {'label':'SPI-2' ,'value': 'spi2'},
           {'label':'SPI-3' ,'value': 'spi3'},
           {'label':'SPI-6' ,'value': 'spi6'},
           {'label':'SPEI-1' ,'value': 'spei1'},
           {'label':'SPEI-2' ,'value': 'spei2'},
           {'label':'SPEI-3' ,'value': 'spei3'},
           {'label':'SPEI-6','value': 'spei6'}]

indexnames = {'noaa': 'NOAA CPC-Derived Rainfall Index',
              'pdsi': 'Palmer Drought Severity Index',
              'pdsisc': 'Self-Calibrated Palmer Drought Severity Index',
              'pdsiz': 'Palmer Z Index',
              'spi1':'Standardized Precipitation Index - 1 month',
              'spi2':'Standardized Precipitation Index - 2 month',
              'spi3':'Standardized Precipitation Index - 3 month',
              'spi6':'Standardized Precipitation Index - 6 month',
              'spei1': 'Standardized Precipitation-Evapotranspiration Index - 1 month', 
              'spei2': 'Standardized Precipitation-Evapotranspiration Index - 2 month', 
              'spei3': 'Standardized Precipitation-Evapotranspiration Index - 3 month', 
              'spei6': 'Standardized Precipitation-Evapotranspiration Index - 6 month'}

# This is for accessing the dataset
returns = [{'label':'Potential Producer Premiums','value':'premiums'},
          {'label':'Potential Indemnities','value':'indemnities'},
          {'label':'Potential Payout Frequencies','value':'frequencies'},
          {'label':'Potential Payment Calculation Factors','value':'pcfs'},
          {'label':'Potential Net Payouts','value':'nets'},
          {'label':'Potential Loss Ratios','value':'lossratios'}]

# This is for labeling
returndict = {'premiums':'Potential Producer Premiums',
               'indemnities':'Potential Indemnities',
               'frequencies':'Potential Payout Frequencies',
               'pcfs':'Potential Payment Calculation Factors',
               'nets':'Potential Net Payouts',
               'lossratios':'Potential Loss Ratios'}

# Strike levels
strikes = [{'label':'70%','value':.70},
          {'label':'75%','value':.75},
          {'label':'80%','value':.80},
          {'label':'85%','value':.85},
          {'label':'90%','value':.90}]

# Data Frame Column Names
dfcols = [{'label':"D.I.: Drought Index", 'value': 1},
         { 'label':"A.Y.: Actuarial Year", 'value': 2},
         {'label':"I.COV: Index Coefficient of Variance", 'value': 3},
         { 'label':"S: Strike" , 'value': 4},
         { 'label':" B.R.: Baseline Year Range", 'value': 5},
         { 'label':"S.R.: Study Year Range", 'value': 6},
         { 'label':"T.S.: Temporal Scale", 'value': 7},
         { 'label':"Max P.($): Max Payment", 'value': 8},
         { 'label':"Min P.($): Minimum Payment", 'value': 9},  
         { 'label':"Med P.($): Median Payment", 'value': 10},
         { 'label':"Mean P.($): Mean Payment", 'value': 11}, 
         { 'label':"P. SD: Payment Standard Deviation", 'value': 12}, 
         { 'label':"M.P.SD: Monthly Payment Standard Deviation", 'value': 13},
         { 'label':"Mean PCF: Mean Payment Calculation Factor", 'value': 14},
         { 'label':"PCFSD: Payment Calculation Factor Standard Deviation", 'value': 15},
         { 'label':"M. PCF SD: Monthly Payment Calculation Factor Standard Deviation", 'value': 16},
         { 'label':"Mean P.F.: Mean Payout Frequency", 'value': 17},
         { 'label':"M.P.FSD: Monthly Payout Frequency Standard Deviation", 'value': 18}]

# Create Coordinate Index - because I can't find the array position in the 
# click event!
xs = range(300)
ys = range(120)
lons = [-130 + .25*x for x in range(0,300)]
lats = [49.75 - .25*x for x in range(0,120)]
londict = dict(zip(lons, xs))
latdict = dict(zip(lats, ys))
londict2  = {y:x for x,y in londict.items()} # This is backwards to link simplified column 
latdict2  = {y:x for x,y in latdict.items()} # This is backwards to link simplified column 

# Create global chart template
mapbox_access_token = 'pk.eyJ1IjoidHJhdmlzc2l1cyIsImEiOiJjamZiaHh4b28waXNkMnptaWlwcHZvdzdoIn0.9pxpgXxyyhM6qEF_dcyjIQ'

# Map Layout:
layout = dict(
    autosize=True,
    height=500,
    font=dict(color='#CCCCCC'),
    titlefont=dict(color='#CCCCCC', size='20'),
    margin=dict(
        l=35,
        r=35,
        b=65,
        t=65
    ),
    hovermode="closest",
    plot_bgcolor="#e6efbf",
    paper_bgcolor="#083C04",
    legend=dict(font=dict(size=10), orientation='h'),
    title='<b>Potential Payout Frequencies</b>',
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
        # Title and Image
                html.Img(
                    src = "https://github.com/WilliamsTravis/Pasture-Rangeland-Forage/blob/master/data/earthlab.png?raw=true",
#                    src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe.png",
                    className='one columns',
                    style={
                        'height': '150',
                        'width': '300',
                        'float': 'right',
                        'position': 'static',
                    },
                ),
                html.Img(
                    src = "https://github.com/WilliamsTravis/Pasture-Rangeland-Forage/blob/master/data/CU_Boulder.jpg?raw=true",
#                    src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe.png",
                    className='one columns',
                    style={
                        'height': '150',
                        'width': '300',
                        'float': 'right',
                        'position': 'static',
                    },
                )],
                className = 'row'
                ),
        html.Div(# One
            [
                html.H1(
                    'Index Insurance Exploratory Analysis Tool:',
                    className='eight columns',
                ),
                html.H2(
                         'The Pasture Rangeland and Forage with a drought index?',
                         className = ' eight columns'
                ),
            ],
            className='row'
        ),
        # Year Slider Text 
        html.Div(# Two
            [
                html.H5(
                    '',
                    id='year_text',
                    className='six columns',
                    style={'text-align': 'left'}
                ),

#                html.H5(
#                    '',
#                    id='year_text2',
#                    className='two columns',
#                    style={'text-align': 'center'}
#                ),                
            ],
            className='row'
        ),
        # Year Sliders 
        html.Div(
            [
                html.P('Study Period Year Range'),  
                dcc.RangeSlider(
                    id='year_slider',
                    value=[2000, 2017],
                    min=2000,
                    max=2017,
                ),
#                html.P('Baseline Average Year Range'), 
#                dcc.RangeSlider(
#                    id='year_slider2',
#                    value=[1948, 2016],
#                    min=1948,
#                    max=2017
#                ),
            ],
            style={'margin-top': '20'}
        ),
            
        # Selections
        html.Div(# Four
            [
                # Dropdowns
                html.Div(# Four-a
                    [
                        html.P('Drought Index'),
                        dcc.Dropdown(
                            id = 'index_choice',
                            options = indices,                            
                            value = "noaa",
                            placeholder = "NOAA CPC-Derived Rainfall Index"
                        ),
                        html.P('Choose Information Type'),
                        dcc.Dropdown(
                            id = 'return_type',
                            value = 'indemnities',
                            multi = False,
                            options = returns
                        ),
#                        html.P('Number of Acres'),
#                        dcc.Input(
#                            id = 'acres',
#                            placeholder = 'Number of acres...',
#                            value = 500,
#                            type = 'number'
#                            )                   
                        ],
                    className='four columns'
                ),
                            
                # Other Selections
                html.Div(# Four-a
                    [
                        html.P('Guarantee Level'),
                        dcc.RadioItems(
                            id='strike_level',
                            options=strikes,
                            value=.75,
                            labelStyle={'display': 'inline-block'}
                        ),                        
                        html.P('Actuarial Year'),
                        dcc.RadioItems(
                            id='actuarial_year',
                            value=2018,
                            options=[{'label':'2017','value':2017},
                                      {'label':'2018','value':2018}],
                            labelStyle={'display': 'inline-block'}
                        ),

                        html.Button(id='submit', type='submit', n_clicks = 0, children='submit')

                    ],
                    className='four columns'
                ),
               ],
                className = 'row'
            ),
        # Hidden DIV to store the signal 
        html.Div(id='signal',
                 style={'display': 'none'}
#                 children = ['noaa',2018,[2000, 2017],[1948, 2016], 0.8, 500,"indemnities"]
            ),
        # Single Interactive Map
        html.Div(#Five
            [
                html.Div(#Five-a
                    [
                        dcc.Graph(id='main_graph'),
                        html.Button(id='map_info',
                                    title = mapinfo,
                                    type='button', 
                                    n_clicks = 0, 
                                    children='Map Info \uFE56 (Hover)'),
                    ],
                    className='seven columns',
                    style={'margin-top': '40'}
                ),
                html.Div(# Five-b
                    [
                        dcc.Graph(id='trend_graph'),
                        html.Button(id='trend_info', 
                                    type='button',
                                    title = trendinfo,
                                    n_clicks = 0, 
                                    children='Trend Info \uFE56 (Hover)'),
                    ],
                    className='five columns',
                    style={'margin-top': '40'}
                )
            ],
            className='row'
        ),
        # Time-Series and histogram
        html.Div(#Six
            [
                html.Div(#Six-a
                    [
                        dcc.Graph(id='series_graph'),
                        html.Button(id='series_info',
                                    type='button',
                                    title = seriesinfo,
                                    n_clicks = 0, 
                                    children='Time Series Info \uFE56 (Hover)'),
                    ],
                    className='twelve columns',
                    style={'margin-top': '10'}
                ),
#                html.Div(#Six-a
#                    [
#                        dcc.Graph(id='histogram')
#                    ],
#                    className='six columns',
#                    style={'margin-top': '10'}
#                ),                
            ],
            className='row'
        ),
        # Data chart
        html.Div(#Seven
            [
                html.Div(
                    [   html.H1(" "),                      
                        html.H4('Summary Statistics'),
                        html.H5("Column Key"),
                        dcc.Dropdown(options = dfcols,
                                     placeholder = "Acronym: Description"),
                        dt.DataTable(
                             rows = datatable,
                             id = "summary_table",
                             filterable=True,
                             sortable=True,
                             row_selectable=True,
#                             min_width = 1655,
                             )
                    ],
                    className='twelve columns',
                    style={'width':'100%', 'display': 'inline-block', 'padding': '0 20'},
                ),             
            ],
            className='twelve columns'
        ),
    ],
    className='ten columns offset-by-one'
  )
        


# In[]:
############################################################################### 
######################### Create Cache ######################################## 
############################################################################### 
@cache.memoize()
# Next step, create a numpy storage unit to store previously loaded arrays
def global_store(signal):
    # Unjson the signal (Back to original datatypes)
    signal = json.loads(signal)

    # Rename signals for comprehension
    rasterpath = signal[0]
    actuarialyear = signal[1]
    studyears = signal[2] # No study years yet :/
#    baselineyears = signal[3]
    strike = signal[3]
#    acres = signal[4]
    returntype = signal[4]     
  
    if test == False:
        # Average Map
        averagepath = ("onlinedata/AY"
                   + str(actuarialyear) + "/"+str(int(strike*100)) + "/"+str(returntype)
                   +"/"+rasterpath+"/array.npz") # This is where it breaks, because there is no rasterpath at first
        
        # Time-series path
        timeseriespath = ("onlinedata/AY"
                   + str(actuarialyear) + "/"+str(int(strike*100)) + "/"+str(returntype)
                   +"/"+rasterpath+"/arrays.npz")
        
        # Dates and Index name Path
        datepath = ("onlinedata/AY"
                   + str(actuarialyear) + "/"+str(int(strike*100)) + "/"+str(returntype)
                   +"/"+rasterpath+"/dates.csv")
        
        # Get with getNPY and getNPYs
        array = getNPY(averagepath)
        arrays = getNPYs(timeseriespath,datepath)
        arrays.append(array) # Now the average is last, call it with [-1]
        df = arrays
    else:
        # Average Map
        averagepath = ("D:\\data\\prfpayouts\\onlinedata\\AY"
                   + str(actuarialyear) + "\\"+str(int(strike*100)) + "\\"+str(returntype)
                   +"\\"+rasterpath+"\\array.npz")
        
        # Time-series path
        timeseriespath = ("D:\\data\\prfpayouts\\onlinedata\\AY"
                   + str(actuarialyear) + "\\"+str(int(strike*100)) + "\\"+str(returntype)
                   +"\\"+rasterpath+"\\arrays.npz")
        
        # Dates and Index name Path
        datepath = ("D:\\data\\prfpayouts\\onlinedata\\AY"
                   + str(actuarialyear) + "\\"+str(int(strike*100)) + "\\"+str(returntype)
                   +"\\"+rasterpath+"\\dates.csv")
        
        # Get numpy arrays
        array = np.load(averagepath)
        array = array.f.arr_0    
        datedf = pd.read_csv(datepath)
        arrays = np.load(timeseriespath)
        arrays = arrays.f.arr_0    
        arrays = [[datedf['dates'][i],arrays[i]] for i in range(len(arrays))]
        arrays.append(array) # Now the average is last, call it with [-1]
        df = arrays

    return df
        
def retrieve_data(signal):
    if str(type(signal)) == "<class 'NoneType'>":
        signal = source_signal
    df = global_store(signal)
    return df


###############################################################################
########################### Get Signal ########################################
###############################################################################
# Store the data in the cache and hide the signal to activate it in the hidden div
@app.callback(Output('signal', 'children'), 
              [Input('submit','n_clicks')],
              [State('index_choice', 'value'),
               State('actuarial_year','value'),
               State('year_slider','value'),
#               State('year_slider2','value'),
               State('strike_level','value'),
#               State('acres','value'),
               State('return_type','value')])
def compute_value(clicks,index_choice,actuarial_year,year_slider,strike_level,returntype):
    signal = json.dumps([index_choice,actuarial_year,year_slider,strike_level,returntype])
    return signal


# In[] 
############################################################################### 
######################### Create Callbacks #################################### 
############################################################################### 
# Other Call Backs
 # Slider1 -> Base line Year text
@app.callback(Output('year_text', 'children'),
              [Input('year_slider', 'value')])
def update_year_text(year_slider):
    return "Study Period: {} | {} ".format(year_slider[0], year_slider[1])

# Button2 -> Map Info Text
@app.callback(Output('map_info', 'title'),
              [Input('signal', 'children')])
def update_mapinfo(signal):
    # For the strike level
    if not signal:
        signal = source_signal
    signal = json.loads(signal)
    strike_level = signal[3]
        # Description for Info Button:
    mapinfo = (" This map shows the average amount of payout potential at each of the available "
               "grid cells using the experimental index insurance program with a 50% allocation of "
               "total protection to each insurance interval  from a hypothetical policy on a 500 "
               "acre ranch at the "+ str(int(strike_level*100)) + "% Strike Level and 100% "
               "productivity level.")
    return mapinfo

# Button3 -> Trend Info Text
@app.callback(Output('trend_info', 'title'),
              [Input('signal', 'children'),
               Input('main_graph','clickData')])
def update_trendinfo(signal,clickData):
    # For the strike level
    if not signal:
        signal = source_signal
    signal = json.loads(signal)
    strike_level = signal[3]
    # For the grid id
    if clickData is None:
        x = londict.get(-100)
        y = latdict.get(40)
        targetid  = grid[y,x]
    else:
        x = londict.get(clickData['points'][0]['lon'])
        y = latdict.get(clickData['points'][0]['lat'])
        targetid  = grid[y,x]    
    targetid = str(int(targetid))

    # Description for Info Button:
    trendinfo = (" This bar chart shows the average monthly amount of payout potential at grid cell #"
                + targetid + " using the experimental index insurance program with a 50% allocation of "
               "total protection to each insurance interval from a hypothetical policy on a 500 "
               "acre ranch at the "+ str(int(strike_level*100)) + "% Strike Level and 100% "
               "productivity level.")
    return trendinfo
    
# Button4 -> Time Series Info Text
@app.callback(Output('series_info', 'title'),
              [Input('signal', 'children'),
               Input('main_graph','clickData')])
def update_seriesinfo(signal,clickData):
    # For the strike level
    if not signal:
        signal = source_signal
    signal = json.loads(signal)
    strike_level = signal[3]
    year1 = signal[2][0]
    year2 = signal[2][1]
    
    # For the grid id
    if clickData is None:
        x = londict.get(-100)
        y = latdict.get(40)
        targetid  = grid[y,x]
    else:
        x = londict.get(clickData['points'][0]['lon'])
        y = latdict.get(clickData['points'][0]['lat'])
        targetid  = grid[y,x]    
    targetid = str(int(targetid))

    # Description for Info Button:
    seriesinfo = (" This is a time series of potential payouts that would have been received between "
                 +  str(year1) + " and " + str(year2) + " at grid cell #"
                + targetid + " using the experimental index insurance program with a 50% allocation of "
               "total protection to each insurance interval from a hypothetical policy on a 500 "
               "acre ranch at the "+ str(int(strike_level*100)) + "% Strike Level and 100% "
               "productivity level.")
    
    return seriesinfo
# In[]
###############################################################################
######################### Graph Builders ######################################
###############################################################################
@app.callback(Output('main_graph', 'figure'),
              [Input('signal','children')]) 
def makeMap(signal):
    """
    This will be the map itself, it is not just for changing maps.
        In order to map over mapbox we are creating a scattermapbox object.
    """  
    # Get data
    df = retrieve_data(signal)
    
    # Get only the last array
    df = df[len(df)-1]
  
    # Get signal for labeling    
    signal = json.loads(signal)
    return_type = signal[4]
    strike_level = signal[3]
    
    # Data symbol for hover data
    if return_type == "premiums" or return_type == "indemnities" or return_type == "nets":
        datasymbol = "$"
    else:
        datasymbol = ""
        
    # Second, convert data back into an array, but in a from xarray recognizes
    array = np.array([df],dtype = "float32")
    
    # Third, change the source array to this one. Source is defined up top
    source.data = array
    
    # Fourth, bin the values into lat, long points for the dataframe
    dfs = xr.DataArray(source, name = "data")
    pdf = dfs.to_dataframe()
    step = .25
    to_bin = lambda x: np.floor(x / step) * step
    pdf["latbin"] = pdf.index.get_level_values('y').map(to_bin)
    pdf["lonbin"] = pdf.index.get_level_values('x').map(to_bin)   
    pdf['gridx']= pdf['lonbin'].map(londict)  
    pdf['gridy']= pdf['latbin'].map(latdict)  
    grid2 = np.copy(grid)
    grid2[np.isnan(grid2)] = 0
    pdf['grid'] = grid2[pdf['gridy'],pdf['gridx']]
    pdf['grid'] = pdf['grid'].apply(int)
    pdf['grid'] = pdf['grid'].apply(str)
    pdf['printdata'] =  "<br>Data: "+datasymbol+pdf.apply(lambda x: x['data'] if pd.isnull(x['data']) else "{:,}".format(round(x['data'])), axis=1)#.apply(str)
    pdf['wordgrid'] = "GRID #: "
    pdf['grid2'] = pdf['wordgrid'] + pdf['grid'] +pdf['printdata']
    groups = pdf.groupby(("latbin", "lonbin"))
    df_flat = pdf.drop_duplicates(subset=['latbin', 'lonbin'])
    df= df_flat[np.isfinite(df_flat['data'])]
    
    # Add Grid IDs
    colorscale = [[0, 'rgb(2, 0, 68)'], [0.25, 'rgb(17, 123, 215)'],# Make darker (pretty sure this one)
                    [0.35, 'rgb(37, 180, 167)'], [0.45, 'rgb(134, 191, 118)'],
                    [0.6, 'rgb(249, 210, 41)'], [1.0, 'rgb(255, 249, 0)']] # Make darker
    

# Create the scattermapbox object
    data = [ 
        dict(
        type = 'scattermapbox',
        lon = df['lonbin'],
        lat = df['latbin'],
        text = df['grid2'],#np.round(df['data'],2),
        mode = 'markers',
        hoverinfo = 'text',
        marker = dict(
            colorscale = colorscale,
            cmin = 0,
            color = df['data'],
            cmax = 25000,#df['data'].max(),
            opacity=0.85,
            colorbar=dict(  
                title=returndict.get(return_type),
                textposition = "auto",
                orientation = "h"
                )
            )
        ), # This will be for a point to be placed on the map, lot's of things to do that
#        dict(
#            type = 'scattermapbox',
#            lon = point['lonbin'],
#            lat = point['latbin'],
#            text = np.round(point['data'],2),
#            mode = 'markers',
#            marker = dict(
#                 size = point['size'],
#                 color = 'rgb(249, 0, 0)'
#                 )
#            )
        ]
     

    # Title Business
    if return_type == 'frequencies':
        calc = "Sum "
    else:
        calc = "Average "
    layout['title'] = "<b>" +indexnames.get(signal[0]) +"<br>" +calc+returndict.get(return_type)+"  |  " +str(signal[2][0]) + " to " + str(signal[2][1])+ "  |  " + str(int(strike_level*100)) + "% Strike Level</b>"
#                
    # Seventh wrap the data and layout into one
    figure = dict(data=data, layout=layout)
#    return {'figure':figure,'info': index_package_all}
    return figure


# In[]
###############################################################################
###############################################################################
###############################################################################
@app.callback(Output('trend_graph','figure'),
               [Input('main_graph','clickData'),
               Input('signal','children')])
def makeTrendBar(clickData,signal):
    '''
    Makes a monthly trend bar for the selected information type at the clicked 
        location.
    '''
    if clickData is None:
        x = londict.get(-100)
        y = latdict.get(40)
        targetid  = grid[y,x]
    else:
        x = londict.get(clickData['points'][0]['lon'])
        y = latdict.get(clickData['points'][0]['lat'])
        targetid  = grid[y,x]
 
    # Get data
    # arrays
    if not signal:
        signal = source_signal
    df = retrieve_data(signal)
    signal = json.loads(signal)

    # Knock of the average array
    df = df[:-1]
    
    # Get signal for labeling
    return_type = signal[4]
    
    # Catch the target grid cell
    index = np.where(grid == targetid)
    
    # Create the time series of data at that gridcell
    timeseries = [[item[0],item[1][index]] for item in df]
    
    # For title
    dates = [int(item[0][-6:-2]) for item in timeseries]
    date1 = str(min(dates)) 
    date2 = str(max(dates))
    
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
    # if return_type = frequencies (8) - use the summation instead of mean
    if return_type == 'frequencies':
        averages =  tuple(np.asarray([np.sum(sublist) for sublist in valuelist]))
        calc = "Sums "
    else:
        averages =  tuple(np.asarray([np.mean(sublist) for sublist in valuelist]))
        calc = "Averages "
        
    intlabels = [months.get(i) for i in range(1,12)]
    x = np.arange(len(intervals))    
    
    layout_count = copy.deepcopy(layout)
    colors = [            
            "#050f51",#'darkblue',
            "#1131ff",#'blue',
            "#09bc45",#'somegreensishcolor',
            "#6cbc0a",#'yellowgreen',
            "#0d9e00",#'forestgreen',
            "#075e00",#'darkgreen',
            "#1ad10a",#'green',
            "#fff200",#'yellow',
            "#ff8c00",#'red-orange',
            "#b7a500",#'darkkhaki',
            "#6a7dfc" #'differentblue'
            ]
    data = [
#        dict(
#            type='scatter',
#            mode='markers',
#            x=x,
#            y=averages,
#            name= returndict.get(return_type),
#            opacity=0,
#            hoverinfo='skip',
#        ),
        dict(
            type='bar',
            marker = dict(color = colors,line = dict(width = 3.5, color = "#000000")),
#            yaxis = dict(range = [0,2500]),
            x=x,
            y=averages    
        ),
    ]
    if max(averages) < 15000:
        yaxis = dict(
                autorange=False,
                range=[0, 15000],
                type='linear'
                )
        annotation = dict(
            text= "",
            x=0.95,
            y=0.95,
            font = dict(size = 17,color = "#000000"),
            showarrow=False,
            xref="paper",
            yref="paper"
        )
    else:
        yaxis = dict(
                autorange = True,
                type = 'linear'
                )
        annotation = dict(
            text= "<b>(rescaled)</b>",
            x=0.95,
            y=0.95,
            font = dict(size = 17,color = "#000000"),
            showarrow=False,
            bgcolor = "#e6efbf",
            xref="paper",
            yref="paper"
        )
        
    
    layout_count['title'] = ("<b>" +returndict.get(return_type)
                             + ' Monthly Trends: '+calc + '<br> Grid ID: '
                             + str(int(targetid)) + "</b>")
    layout_count['dragmode'] = 'select'
    layout_count['showlegend'] = False 
    layout_count['annotations'] = [annotation]
    layout_count['xaxis'] = dict(tickvals = x, ticktext = intlabels)
    layout_count['yaxis'] = yaxis
    figure = dict(data=data, layout=layout_count)
    return figure

# In[]
###############################################################################
######################## Time Series ##########################################
###############################################################################
@app.callback(Output('series_graph','figure'),
               [Input('main_graph','clickData'),
               Input('signal','children')])
def makeSeries(clickData,signal):
    '''
    Just like the trend bar, but for a time series.
    '''
    if clickData is None:
        x = londict.get(-100)
        y = latdict.get(40)
        targetid  = grid[y,x]    

    else:
        x = londict.get(clickData['points'][0]['lon'])
        y = latdict.get(clickData['points'][0]['lat'])
        targetid  = grid[y,x]
    
    
    # Get data
    if not signal:
        signal = source_signal
        
    df = retrieve_data(signal)
    
    # Get the signal for Labeling
    signal = json.loads(signal)
    return_type = signal[4]
    return_label = returndict.get(return_type)
    
    # Knock the average map off
    df = df[:-1]
    
    # For title
    dates = [item[0][-6:-2]+"-"+ item[0][-2:] for item in df]
    intervals = [int(d[-2:]) for d in dates]
    dates1 = str(min(dates)) 
    dates2 = str(max(dates))
            
    # Catch the target grid cell
    index = np.where(grid == targetid)
    
    # Create the time series of data at that gridcell
    values = [float(item[1][index]) for item in df]
    valuesum = "<b>Total: ${:,}".format(int(np.sum(values))) + "</b>"
    
    # Create Seasonal Colors
    colors = {            
        1:"#050f51",#'darkblue',
        2:"#1131ff",#'blue',
        3:"#09bc45",#'somegreensishcolor',
        4:"#6cbc0a",#'yellowgreen',
        5:"#0d9e00",#'forestgreen',
        6:"#075e00",#'darkgreen',
        7:"#1ad10a",#'green',
        8:"#fff200",#'yellow',
        9:"#ff8c00",#'red-orange',
        10:"#b7a500",#'darkkhaki',
        11:"#6a7dfc" #'differentblue'
        }
    
    colors = [colors.get(d) for d in intervals]
    
    annotation = dict(
            text= valuesum,
            x=0.95,
            y=0.95,
            font = dict(size = 17,color = "#000000"),
            showarrow=False,
            xref="paper",
            yref="paper"
        )
        
    data = [
        dict(
            x=dates,        
            y=values,
            type='bar',            
            name= return_label+' Value Ditribution',
            opacity=1,
            hoverinfo='skip',
            marker = dict(color = colors,
                          line = dict(width=1, color = "#000000")
                          )
        ),
#        dict(
#            type='bar',
#            x=bins,
#            y=hists,
#            marker = dict(
#                    color = '#000000'
#            ),
#        ),
    ]
            
    
    if max(values) < 45000:
        yaxis = dict(
                autorange=False,
                range=[0, 45000],
                type='linear'
                )
        annotation = dict(
            text= valuesum,
            x=0.95,
            y=0.95,
            font = dict(size = 17,color = "#000000"),
            showarrow=False,
            bgcolor = "#e6efbf",
            xref="paper",
            yref="paper"
        )
    else:
        yaxis = dict(
                autorange = True,
                type = 'linear'
                )
        annotation = dict(
            text= valuesum +"<br><b> (rescaled)</b>",
            x=0.95,
            y=0.95,
            font = dict(size = 17,color = "#000000"),
            showarrow=False,
            bgcolor = "#e6efbf",
            xref="paper",
            yref="paper"
        )
    layout_count = copy.deepcopy(layout)
    layout_count['title'] = "<b>" + return_label+' Time Series <br> Grid ID: ' + str(int(targetid)) +"</b>"
    layout_count['dragmode'] = 'select'
    layout_count['showlegend'] = False
    layout_count['annotations'] = [annotation]
    layout_count['yaxis'] = yaxis
    
    figure = dict(data=data, layout=layout_count)
        
    return figure

## In[]          
############################ I'll start with just the time series ##############
## It needs to generate a path from signals stored in json format
#signal = source_signal
#jsignal = json.loads(signal)
#
## Rename signals for comprehension
#index = jsignal[0]
#actuarialyear = jsignal[1]
#studyears = jsignal[2]
#baselineyears = jsignal[3]
#strike = jsignal[4]
#acres = jsignal[5]
#returntype = jsignal[6]
#
## Generate AWS Paths and get arrays
#testpath = "onlinedata/arrays_test.npz"
#
## Average Map
#averagepath = ("onlinedata/AY"
#           + str(actuarialyear) + "/"+str(int(strike*100)) + "/"+str(returntype)
#           +"/"+index+"/array.npy")
#
## Time-series path
#timeseriespath = ("onlinedata/AY"
#           + str(actuarialyear) + "/"+str(int(strike*100)) + "/"+str(returntype)
#           +"/"+index+"/arrays.npy")
#
## Dates and Index name Path
#datepath = ("onlinedata/AY"
#           + str(actuarialyear) + "/"+str(int(strike*100)) + "/"+str(returntype)
#           +"/"+index+"/dates.csv")
#
#
## Read in arrays and dates - https://stackoverflow.com/questions/48964181/how-to-load-a-pickle-file-from-s3-to-use-in-aws-lambda
#start = time.clock()
#
## Average Map ~ 1.5 seconds
#testmap = getNPY(averagepath)
#
## Time-series
## Test ~ 10 seconds, we might have to settle
#timeseries = getNPYs(testpath,datepath)
#
## Total ~ 10.5 seconds? 
#end = time.clock() - start       
#print(end)
## In[]:
    
# In[]:
# Main
#if __name__ == '__main__':
#    app.server.run(use_reloader = False, threaded=True)#debug=True

if __name__ == '__main__':
    app.run_server()#threaded=True
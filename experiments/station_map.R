"
Here we flagging auctions that don't close between whenever the start and finish dates are.
"
setwd("c:/users/user/github/Pasture-Rangeland-Forage-Storage/")
source("functions.R")
source("G:/My Drive/THESIS/Final_Figures_Scripts/themes.R")
library(plotly)

############################### Create Shaefile ######################
# Apply the storage rules, they didn't want decimals for some reason/
# LEGEND:
 
# STNID - 5 CHARACTER WMO STATION IDENTIFIER
# LAT   - LATITUDE IN HUNDRETHS, EX:  7093 = 70.93 N, -1093 = 10.93 S
# LON   - LONGITUDE IN HUNDRETHS, EX: 34637 = 346.37
# IF LON > 180 LON = 360 - LON ****(wtf)
# ELEV  - STATION ELEVATION IN WHOLE METERS
# CALL  - STATION IDENTIFICATION CALL LETTERS IF AVAILABLE


# # Read in dataset
# stations = read.csv("data/weather_stations/cpc_stations.csv")
# 
# # Create Spatial Object
# usa = stations[stations$COUNTRY == "UNITED STATES",]
# 
# # Fix Coordinates
# usa[c(3,4)] = usa[c(3,4)]/100
# usa$LON = ifelse(usa$LON < 180, 360 - usa$LON, usa$LON)
# 
# # change lat lon labels
# colnames(usa)[c(3,4)] = c("y","x")
# usa$X  = NULL
# 
# # Spatialize
# spatialize = function(dfrm){
#   dfrm%<>%na.omit()
#   names(dfrm) = tolower(names(dfrm))
#   xindx = match("x",colnames(dfrm))
#   yindx = match("y",colnames(dfrm))
#   xy = dfrm[,c(xindx,yindx)]
#   srs = "+proj=longlat +datum=NAD83 +no_defs +ellps=GRS80 +towgs84=0,0,0"
#   spdfrm = SpatialPointsDataFrame(coords = xy, data = dfrm, proj4string = CRS(srs))
#   return(spdfrm)
# }
# usa = spatialize(usa)
# 
# 
# # Alber's Equal Area
# # srs = "+proj=aea +lat_1=20 +lat_2=60 +lat_0=40 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m +no_defs"
# # # usa = spTransform(usa,srs)
# 
# states = readOGR("data/shapefiles/USAContiguous.shp")
# 
# # Keep only CONUS - and fix this weird crs
# usa = usa[usa$y < 50 & usa$x > 220 & usa$y > 25,]
# usa2 = usa
# usa2@data$x = usa2@data$x - 360
# names(usa2@coords) = c("x","y")
# usa2@coords[,1] = usa@coords[,1] - 360
# usa2@bbox = states@bbox
# 
# #
# plot(states)
# plot(usa2,add =T,pch = 18)
# 
# 
# writeOGR(usa2, dsn = "data/weather_stations",layer = "weather_stations",driver = "ESRI Shapefile")




############# Interactive map? #########################
states = readOGR("data/shapefiles/USAContiguous.shp")
srs = "+proj=aea +lat_1=20 +lat_2=60 +lat_0=40 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m +no_defs"
states = spTransform(states,srs)
states@data$id = row.names(states@data)
statesdf = fortify(states,region = "id")

stations = readOGR("data/weather_stations/weather_stations.shp")
stations = spTransform(stations,srs)
stations@data[c(2,3)] = stations@coords[,c(2,1)]

points =
  ggplot(data = stations@data,aes(x = x, y = y))+
          geom_path(data = states,aes(x = long, y = lat, id = group))+
          geom_point(aes(text = city,colour = y),alpha = .67)+
          coord_equal()+
          mapTheme()

ggplotly(points)

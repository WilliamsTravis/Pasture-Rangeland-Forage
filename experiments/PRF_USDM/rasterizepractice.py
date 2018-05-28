# -*- coding: utf-8 -*-
"""
Created on Mon May 15 15:52:20 2017

@author: Travis Williams
"""
import sys,os,time, subprocess
import numpy as np
import numpy.ma as ma
from osgeo import ogr, osr, gdal
from tqdm import *
os.chdir('C:\\Users\\Travis\\Desktop\\Data\\droughtindices\\usdm')
gdal.UseExceptions()
print("GDAL version:" + str(int(gdal.VersionInfo('VERSION_NUM'))))


###############################################################################
###########################USDM Projection#####################################
############################################################################### 
# Here I extract all of the rasters from their original folders and put them 
# into one spot

usdmfolder = os.listdir('usdmoriginal')
usdmraster = os.listdir('usdmrasters')
usdmall = os.listdir('usdmall')
usdmout = 'usdmall\\'
usdmin = 'usdmoriginal\\'

inputfolder = os.getcwd()+ '\\usdmoriginal' #type unicode
DirsList = []
for root, dirs, files in os.walk(inputfolder):
    if len(dirs) > 1:
        DirsList.append(dirs)

# Flatten this list of lists (lol) into a single list:
DMs = [item for sublist in DirsList for item in sublist if len(item)>12] # length target folder name =    

       #.shp,.shx,.dbf,.proj,.sbx,.sbn
for i in usdmraster:
    if i[-3:]=="xml":
        os.rename("usdmall\\" + i,"usdmoriginal\\"+i)

###############################################################################
##########################  consol command ####################################
###############################################################################       
    
#for %i in (*.shp) do gdal_rasterize -a DM -l %~ni -a_srs epsg:4269 -a_nodata -9999 -te -130 20 -55 50 -tr 0.25 0.25 %i C:\Users\Travis\Desktop\Data\droughtindices\usdm\usdmrasters\%~ni.gtif    
    
###############################################################################
##########################  subprocess Practice ###############################
############################################################################### 
# Use the strings above to navigate to the appropriate folders and rasterize the 
# shapefiles. This might be the longest step.
start = time.clock()
for i in tqdm(DMs):
    cmd = ['gdal_rasterize', ? , ? ,usdmin + i, usdmout+ i]
    process = subprocess.Popen(cmd, shell = True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
    time.sleep(.01)
end = time.clock() - start       
print("Processing time = " + str(round(end/60,2)) + " minutes")


###############################################################################
########################## OGR Practice #######################################
############################################################################### 

# Import Python 3 print function
from __future__ import print_function

# Open the dataset from the file
dataset = ogr.Open('data\\usdm\\2000\\USDM_20000718_M\\USDM_20000718.shp')

# Make sure the dataset exists -- it would be None if we couldn't open it
if not dataset:
    print('Error: could not open dataset')
 
# What type of thing is it?
driver = dataset.GetDriver()
print('Dataset driver is: {n}\n'.format(n=driver.name))

### How many layers are contained in this Shapefile?
layer_count = dataset.GetLayerCount()
print('The shapefile has {n} layer(s)\n'.format(n=layer_count))

### What is the name of the 1 layer?
layer = dataset.GetLayerByIndex(0)
print('The layer is named: {n}\n'.format(n=layer.GetName()))

### What is the layer's geometry? is it a point? a polyline? a polygon?
# First read in the geometry - but this is the enumerated type's value
geometry = layer.GetGeomType()

# So we need to translate it to the name of the enum
geometry_name = ogr.GeometryTypeToName(geometry)
print("The layer's geometry is: {geom}\n".format(geom=geometry_name))

#proj4 = spatial_ref.ExportToProj4()
#print('Layer projection is: {proj4}\n'.format(proj4=proj4))

### How many features are in the layer?
feature_count = layer.GetFeatureCount()
print('Layer has {n} features\n'.format(n=feature_count))
print('Layer has ' + str(feature_count) + ' features')
### How many fields are in the shapefile, and what are their names?
# First we need to capture the layer definition
defn = layer.GetLayerDefn()

# How many fields
field_count = defn.GetFieldCount()
print('Layer has {n} fields'.format(n=field_count))

print('Their names are: ')
for i in range(field_count):
    field_defn = defn.GetFieldDefn(i)
    print('\t{name} - {datatype}'.format(name=field_defn.GetName(),
                                         datatype=field_defn.GetTypeName()))



# Explanation of switches:
# -a ==> write values from the"id" attribute of the shapefile
# -layer ==> the layer name of our shapefile
# -of ==> Output raster file format
# -a_srs ==> output spatial reference system string
# -a_nodata ==> NODATA value for output raster
# -te ==> target extent which matches the raster we want to create the ROI image for
# -tr ==> target resolution
# -ot Byte ==> Since we only have values 0 - 5, a Byte datatype is enough

gdal_rasterize -a "DM" \
    -layer USDM_20000718 \ #This will be i[0:13]
    -of "AAIGrid" \
    -a_srs "epsg:4269" \
    -a_nodata 0 \
    -te -130 20 -55 50 \ # lower left, upper right
    -tr 0.25 0.25 \
    -ot Byte \
    ../../example/training_data.shp ../../example/training_data.asc
 

    
    
    
    
    cmd = ['gdal_rasterize', ? , ? ,usdmin + i, usdmout+ i]
    process = subprocess.Popen(cmd, shell = True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
    
    cmd = ['gdalwarp', '-a "OBJECTID"','-l USDM_20000718', '-of "GTiff"',  '-a_srs "EPSG:4269"' ,'-a_nodata -9999.0',' -tr 0.25 0.25 ',' -ot Byte ','data\\usdm\\usdmrasters\\test.gtif'] 
    process = subprocess.Popen(cmd, shell = True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
    
    cmd = ['gdalinfo', '-proj4', 'dataset']

thing = subprocess.Popen('ogrinfo -al -so data/usdm/2000/USDM_20000718_M/USDM_20000718.shp',shell = True)   
stdout,stderr=thing.communicate()

ogrinfo -al -so input.shp layer-name
    
    gdalinfo -proj4 ../../example/LE70220491999322EDC01_stack.gtif
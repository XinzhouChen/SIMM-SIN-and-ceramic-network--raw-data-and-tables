#The Python script for Geospatial modelling of farmer-herder interactions maps cultural interactions in Bronze and Iron Age Tibet, 3600-2200 BP
#Run two sections of the codes separately in Python after preparing the input data.
#Prepared by Dr. Xinzhou Chen (xinzhouchen@wustl.edu).

#Import the libraries
import arcpy 
import os
import sys
from arcpy.sa import *


#Setting the workspace
path = ###Supply your path to the workspace (the location of the gdb)
gdb = os.path.join(path, "modis_flow.gdb") #Supply the name of the gdb
cost_raster_grass = os.path.join(gdb,"ndvi_tp_250_norm_flip") # The cost raster of NDVI should be fliped as the flow accumulation method requires.
out_fa_sum_name = "fa_raster_sum_grass_crop_1_6459_highres"# Supply the name of the output Raster.

# Setting the enviroment
arcpy.env.workspace = gdb
arcpy.env.overwriteOutput = True
arcpy.env.scratchWorkspace = gdb


#Seoction 1: Start the iterator from 1, iterate through all cropland points to construct the SIMM.
for n in range(1,6550,1): # the number of total iterations = n (cropland points) + 1.
    
    fc = os.path.join(gdb,"cropland_fao_3km_withinraster_modis") #Supply the feature class of the cropland points.
    #The cropland points used in the LCP analaysis should all in the cost raster otherwise it will lead to a internal error of path tracing
    fc_pt_name = "pt" + str(n) #Supply the name of the single cropland point that was used in each iteration.
    print(fc_pt_name) #Print its name to trace the process of the iterator.
    query =  "OBJECTID = " + str(n) #The query to locate the cropland point using OBJECTID
    fc_pt = arcpy.management.MakeFeatureLayer(fc, "pt_lyr",query) #Mkae a temporary layer of the point to work with.
    output_dist_raster = "codis" #Name of the cost distance raster.
    output_fd_raster = "fd" #Name of the flow direction raster.
    out_fa_raster = "fa" + str(n) #special name for flow accumulation raster.

    #Create cost distance
    out_distance_raster = arcpy.sa.CostDistance(fc_pt, cost_raster_grass, None, None, None, None, None, None, '');
    out_distance_raster.save(output_dist_raster)

    #Create flow direction
    out_flow_direction_raster = arcpy.sa.FlowDirection(output_dist_raster, "NORMAL", None, "D8");
    out_flow_direction_raster.save(output_fd_raster)

    #Create flow accumulation raster
    out_accumulation_raster = arcpy.sa.FlowAccumulation("fd", None, "FLOAT", "D8");
    out_accumulation_raster.save(out_fa_raster)
    
#Sum up the resulting rasters.
outCellStatistics = CellStatistics(rasterlist, "SUM", "NODATA")

#Save the output. 
outCellStatistics.save(out_fa_sum_name)



#Section 2: This part of the code shows how SIN was created.The SIN is a matrix,
#The program iterates through the selected real arcaheological sites and finds the shortest flow distance among them.
#Before using this code, the user should prepare an excelsheet of a matrix that contains n rows and n columns (n = the number of archaeological sites) and export this sheet as a feature class in the gdb.
#The row head of the matrix should be different with the col head, although they represent the same archaeological sites. Here I supply an "F" before each number
#Because ArcGIS pro does not allow repeated row and col names.
#Before using this code, the user should also flip the "out_fa_sum_name" raster, since it will be used as the cost raster in the SIN and larger values of SIMM should be easier to travel across in the SIN.


#Resetting variables in this code.
cost_raster = os.path.join(gdb,"fa_raster_sum_grass_crop_1_6459_highres_flip") #the cost raster is the fliped raster in the SIMM.
fc = os.path.join(gdb,"network_sites") #Supply the location of the feature class that contains the archaeological sites for the network analysis.
table = os.path.join(gdb,"table_matrix") # The feature class of the excelsheet that contains a blank matrix to work with.

#Start the iterator n of iteration 26 (n=the number of archaeological sites)
for n in range(1,26,1):
    output_dist_raster = "dis_raster"
    output_bklink = "bklink"
    print(str("iteration_") + str(n))
    pt_origin_query = "OBJECTID" + "=" + str(n)
    pt_origin = arcpy.management.MakeFeatureLayer(fc, "pt_origin", pt_origin_query)

    #Create cost distance using the raster of the SIMM
    out_distance_raster = arcpy.sa.CostDistance(pt_origin,cost_raster, None, output_bklink, None, None, None, None, '');
    out_distance_raster.save(output_dist_raster)

    #Create the Matrix using the Cost Path as Polyline function in ArcGIS
    for m in range(1,26,1):
        if m != n:
            print(m)
            field_dest =["F" +str(m)]
            print(field_dest)
            outpath = "path"  
            pt_dest_query = "OBJECTID" + "=" + str(m)
            pt_dest = arcpy.management.MakeFeatureLayer(fc, "pt_dest", pt_dest_query)
            path = CostPathAsPolyline(pt_dest, output_dist_raster, output_bklink, outpath)
        
            with arcpy.da.SearchCursor(outpath, ['PathCost'])as cursor1:
                for row in cursor1:
                    value = row[0]

            with arcpy.da.UpdateCursor(table,field_dest,pt_origin_query) as cursor2:
                for row in cursor2:
                    row[0] = value
                    print(row[0])
                    cursor2.updateRow(row)


            cursor3.updateRow(row)

#The result of SIN is a matrix that contains the shortest flow distance between every pair of sites, which requires furthur cleaning such as adding site names. The data cleaning can be done in Excel.

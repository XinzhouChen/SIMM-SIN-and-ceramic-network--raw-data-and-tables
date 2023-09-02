#########

Read this txt file before using the code and data in the Github folder.

Prepared by Xinzhou Chen (xinzhouchen@wustl.edu)

#########
This Github folder contains the data and code for the paper
"Geospatial modelling of farmer-herder interactions maps cultural interactions in Bronze and Iron Age Tibet, 3600-2200 BP"

#File description
Dataset 1 contains the geolocated archaeological sites in Tibet (3600-2200 BP) and the simulated flow values and distances to pathways.
Dataset 2 contains the presence and absence of ceramic attributes from 26 sites to construct the ceramic network.
Dataset 3 contains the Jaccard Index calculated from Dataset 2.
The csv file "Model evaluation" contains randomly generated points to compare with archaeological sites. This file should be used as the input of the "ZscoreandTtest" R script.
The Python code SIMM and SIN shows the workflow of those two models (the code only shows the logic of the models and is not executable as the way it is. It should be splitted into two sections to properly function; see comments in the py file)
The R code "Zsocre_Ttest" provides the code for the statistical evaluation of the results.

######
The comments in R and Python scripts shows how to execute the codes. 

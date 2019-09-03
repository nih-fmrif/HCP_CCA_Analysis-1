#!/usr/bin/python3

#usage: to generate the vars.txt file used by Smith et al. in their analysis
#see here for reference: https://www.fmrib.ox.ac.uk/datasets/HCP-CCA/

# command line arguments need to be as follows:
# argv[1] = column_headers.txt
# argv[2] = filenames.txt
# argv[3] = behavioral data
# argv[4] = restricted data
# argv[5] = rfMRI_motion
# argv[6] = quarter/release info

# Generating the vars.txt:
# To try to make it as easy as possible to generate the appropriate data matrix from these two HCP data files (to match what was fed into our CCA), we include here the file column_headers.txt, which describes how to organise the columns when generating the "vars" subjectsXsubject-measures matrix used in our CCA (see code below). This column_headers file has one text string per row; each entry corresponds to one column in "vars", and matches the appropriate column heading in the two original HCP data files described above.

# Other information needed is:
# A) The "rfMRI_motion" summary head motion file, including subject IDs, is here (column 2 of this needs to become column 7 in "vars.txt").
# B) The "quarter/release" information about recon-code-version is here, with the rows ordered according to the same set of subject IDs as in the head motion file (this needs to become column 2 in "vars.txt").

import numpy as np
import pandas as pd
from pandas import DataFrame
from numpy import genfromtxt
import os
import sys
from pprint import pprint

col_headers_file = sys.argv[1]
filenames_file = sys.argv[2]
behavioral_data_file = sys.argv[3]
restricted_data_file = sys.argv[4]
# rfMRI_data_file = sys.argv[5]
# varsQconf_file = sys.argv[6]
cwd = os.getcwd()

# get the column headers, filenames
col_header_array = [line.rstrip('\n') for line in open(os.path.join(cwd,col_headers_file))]
filenames = [line.rstrip('.pconn.nii\n') for line in open(os.path.join(cwd,filenames_file))]

# now get "behavioral" and "restricted" datasets
# note that these have data on many more subjects than the 461 used in the Smith et al study
behavioral_data = pd.read_csv(os.path.join(cwd, behavioral_data_file))
restricted_data = pd.read_csv(os.path.join(cwd, restricted_data_file))
print('behavior shape before', behavioral_data.shape)
print('shape of restricted before', restricted_data.shape)

#filter the behavioral and restricted datasets to contain only the relevant 461 subject data
behavioral_data = behavioral_data[behavioral_data['Subject'].isin(filenames)]
restricted_data = restricted_data[restricted_data['Subject'].isin(filenames)]


# print('behavior shape after', behavioral_data.shape)
# print('shape of restricted after', restricted_data.shape)

for sub in filenames:
	if(behavioral_data[behavioral_data['Subject'].contains(sub)]):
		continue
	else:
		print('ERROR, subject not found:' + sub)

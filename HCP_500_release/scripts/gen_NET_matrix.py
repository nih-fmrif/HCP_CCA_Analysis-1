#!/usr/bin/python3

# usage: python3 gen_matrixN1.py <path to .txt files with partial parcellations>
# Note, the output file will go same location as the original .txt files with the specified name

import numpy as np
from numpy import genfromtxt
import os
import sys


file_path = sys.argv[1] #path to the folder containing the .txt files w/ matrices
arr_size = sys.argv[2] #number of ICA components (ex. 200)
out_name = sys.argv[3] #what HCP dataset is being used (output filename, ex. HCP_1200_NET.txt)

myList = []

for filename in os.listdir(file_path):
	if filename.endswith(".txt"): 
		#print(os.path.join(file_path, filename))
		arr = genfromtxt(os.path.join(file_path, filename), delimiter=',')

		if(arr.shape[0]==int(arr_size) & arr.shape[1]==int(arr_size)):
			#print("okay file"20, filename)
			flat_lower_tri = arr[np.tril(arr, -1) !=0]
			myList.append(flat_lower_tri)
		else:
			print("ERROR: Incorrect array dimensions in file ", filename)
			continue
	else:
		continue

matrix = np.array(myList)
print("Resulting matrix shape:" ,matrix.shape)
np.savetxt(fname=out_name, X=matrix, delimiter=',')

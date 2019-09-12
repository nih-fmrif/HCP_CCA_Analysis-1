# Human Connectome Project, CCA Analyses

## GOALS

The purpose of this analysis is to:

**(1)** Replicate the results of [Smith et al 2015](https://www.fmrib.ox.ac.uk/datasets/HCP-CCA/).

**(2)** Run this analysis on the larger HCP 1200 patient dataset

**(3)** Create a clean, simple to use pipeline so others can replicate our analysis

**(4)** Expand this analysis to other connectome datasets

# DOCUMENTATION

## Analysis 1 - Attempt to replicate Smith et al. (with 460 subjects)
_All scripts for this analysis are located in analysis1/scripts_

**TO REPLICATE THIS ANALYSIS: you must use the _hcp_cca_analysis1.m_ script along with the _hcp_cca_analysis1.mat_ file.**

**only 460 subjects were used (Smith et al. used 461) because subject 142626 was a duplicate - in a follow up analysis (Analysis 2, discussed below) we will try to exactly replicate with all 461 subjects and the restricted/behavioral data released in the HCP 500 dataset**

1. The subjects x partial connectome matrix was generated   
   - This matrix had to be created from the partial netmat information that is included in the HCP500 release. These are included as CIFTI files (.pconn.nii) which can be opened in HCP Workbench (specifically, in 'wb_view')
      - the specific files used were located in 
                    
            
            HCP_500_release/HCP500_Parcellation_Timeseries_Netmats/netmats_3T_Q1-Q6related468_MSMsulc_ICAd200_ts2.tar.gz
           
            
         _once you extract this file, a folder called 'netmats' is created, the actual CIFTI files needed are located in:_
            
            HCP_500_release/HCP500_Parcellation_Timeseries_Netmats/netmats/3T_Q1-Q6related468_MSMsulc_d200_ts2_netmat2
            
       - because the data is supplied as CIFTI files, HCP workbench's wb_command tool is used to convert them to .csv files
                
            _NOTE: There is a script included in this repo to accompish this, see [get_matrices.sh](https://github.com/Ngoyal95/HCP_CCA_Analysis/blob/master/analysis1/scripts/get_matrices)_
                
   - after generating the CSV files with 200x200 node edge weight data, a python script was used to generate a CSV text file (called 'NET.txt') containing the 460x199000 matrix, to be fed into CCA as in Smith et al.

2. The subject-measure matrix was created using the rfMRI and quarter/release data on the [HCP-CCA site](https://www.fmrib.ox.ac.uk/datasets/HCP-CCA/), the restricted and behavioral (unrestricted) datasets from HCP, and the list of subjectIDs and subject measures provided on that site
   - The resulting matrix was 460x478 (460 subjects, 478 subject measures as listed in the column_headers.txt file on the HCP-CCA site) and outputted to a CSV text file ('vars.txt')
3. The analysis was re-run using the provided hcp_cca.m [code](https://www.fmrib.ox.ac.uk/datasets/HCP-CCA/hcp_cca.m)
   - the following data was used:
      - the NET.txt file
      - the vars.txt file
      - the unrestricted data currently available from the HCP 1200 release (it contains info on 1207 subjects)
      - the restricted data currently available from the HCP 1200 release (contains info on 1207 subjects)
      - the quarter/release [varsQconf file](https://www.fmrib.ox.ac.uk/datasets/HCP-CCA/varsQconf.txt) provided on the HCP-CCA site
      - the [rfMRI_motion.txt](https://www.fmrib.ox.ac.uk/datasets/HCP-CCA/rfMRI_motion.txt) file provided on HCP-CCA site
   
   - the analysis ran successfully, resulting in the following plot of the subject measure CCA weights vs. connectome CCA weights:
   
**The results of this analysis are as follows:**

Ncca (number of FWE-significant CCA components): 0
Scatter plot of SM weights vs. connectome weights for canonical variables:
<p align="center">
  <img src="analysis1/images/analysis1_VvsU.png" alt="plot of canonival variables (subject measures vs. connectome edges)">
</p>

However, this plot is NOT identical to the one in the Smith et al. paper. This could be due to a number of factors (different restricted or behavioral data since we used the data from HCP 1200, the duplicate subject removed)


## Analysis 2 -  Attempt to replicate Smith et al. _exactly_ with 461 subjects
_All scripts for this analysis are located in analysis2/scripts_

**TO REPLICATE THIS ANALYSIS: you must use the _hcp_cca_analysis2.m_ script along with the _hcp_cca_analysis2.mat_ file.**

To exactly replicate the Smith et al study we used:
  - the rfMRI_Motion and quarter/release data provided on the [HCP-CCA site](https://www.fmrib.ox.ac.uk/datasets/HCP-CCA/)
  - the HCP 500 release netmat data to generate NET.txt (same as Analysis 1)
  - the restricted and behavioral files from the HCP 500 release (which should be the exact same as the data used in the Smith et al. study) (in Analysis 1, we used this data from the current release, which could differ from the HCP 500 release)

1. the NET.txt and vars.txt files were generated in the exact same manner as in Analysis 1 (except now with all 461 subjects used by Smith et al., and using slightly different Python scripts, located in analysis2/scripts/)
2. The same hcp_cca.m code was used for analysis
3. Running the code resulted in the following error:

```
Error using canoncorr (line 72)
X and Y must have the same number of rows.

Error in hcp_cca (line 82)
  [grotAr,grotBr,grotRp(j,:),grotUr,grotVr,grotstatsr]=canoncorr(uu1,uu2(PAPset(:,j),:));
```

The input matrix dimensions are:
   - _uu1_ 461x100
   - _uu2_ 461x100
   - _PAPset_ 458x10,000

It looks like the issue is with PAPset, which is generated by the following lines of code: (around line 25)
```
Nperm=10000; % in the paper we used 100000 but 10000 should be enough
EB=hcp2blocks('restricted_500_release.csv', [ ], false, vars(:,1)); % change the filename to your version of the restricted file
PAPset=palm_quickperms([ ], EB, Nperm);       
```

The matrix _EB_ has dimensions 458x5, and appears to be the source of error (the _vars_ matrix has the correct dimensions of 461x478).

It turns out that subjects are being dropped from the restricted data file because they are lacking elementary data necessary to generate the permutations. These subjects are: 108525, 116322, 146331, 256540.

**The MATLAB code was modified to drop these subjects from the analysis and proceed with the subset of 458.**

**The updated MATLAB code to run this analysis is: hcp_cca_analysis2.m**

**The results of this analysis are as follows:**

Ncca (number of FWE-significant CCA components): 0
Scatter plot of the subject measure CCA weights vs. connectome CCA weights:
<p align="center">
  <img src="analysis2/images/analysis2_VvsU.png" alt="plot of canonival variables (subject measures vs. connectome edges)">
</p>

But this is still not identical to the plot of SM weights vs. connectome weights in the Smith et al 2015 paper:
<p align="Center">
  <img src="images/smith_SMsvsConnectome.png" width=450>
</p>


## Analysis 3 - First attempt to expand the CCA analysis to the HCP 1200 dataset with al 478SMs (imputed missing data)
_All scripts for this analysis are located in analysis3/scripts_

**TO REPLICATE THIS ANALYSIS: you must use the _hcp_cca_analysis3.m_ script along with the _hcp_cca_analysis3.mat_ file.**

For this analysis, we lack the rfMRI_Motion and quarter/release (aka varsQconf) data used by Smith et al. These data will be substituted with 0's.

The following data were used:
  - HCP 1200 netmats (to generate the NET matrix, using the script _generate_NET_analysis3.ipynb_)
  - HCP 1200 behavioral and restricted datasets (to generate the subject measure matrix, using script _generate_vars_analysis3.ipynb_)
  - the [column_headers.txt](https://www.fmrib.ox.ac.uk/datasets/HCP-CCA/column_headers.txt) file from the [HCP-CCA site](https://www.fmrib.ox.ac.uk/datasets/HCP-CCA/) (so that the same subject measures are used)
  
Since Smith et al. provided the 478 Subject measures initially fed into the CCA, the vars matrix generated for this analysis uses all 478 measures (imputing missing data when necessary, ex. for the rfMRI_motion and quarter/release data).

Steps:
1. NET.txt and vars.txt were generated using the Jupyter Notebook scripts _generate_NET_analysis3.ipynb_ and _generate_vars_analysis3.ipynb_
2. The MATLAB script hcp_cca_analysis3.m was run (NOTE: the same issue with subjects being dropped is encountered, so the script removes these subjects from our vars and NET matrices)

**The results are as follows:**

Ncca (number of FWE-significant CCA components): 12
Scatter plot of SM weights vs. connectome weights:
<p align="Center">
  <img src="analysis3/images/analysis3_VvsU.png">
</p>


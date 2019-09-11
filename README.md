# Human Connectome Project, CCA Analyses

## GOALS

The purpose of this analysis is to:

**(1)** Replicate the results of [Smith et al](https://www.fmrib.ox.ac.uk/datasets/HCP-CCA/).

**(2)** Run this analysis on the larger HCP 1200 patient dataset

**(3)** Create a clean, simple to use pipeline so others can replicate our analysis

**(4)** Expand this analysis to other connectome datasets

Progress:
- [ ] Goal 1
- [ ] Goal 2
- [ ] Goal 3
- [ ] Goal 4

## DOCUMENTATION

ATTEMPT 1 to replicate Smith et al.:

**only 460 subjects were used (Smith et al. used 461) because subject 142626 was a duplicate - in a follow up analysis we will try to exactly replicate with all 461 subjects and the restricted/behavioral data released in the HCP 500 dataset**

1. The subjects x partial connectome matrix was generated   
   - This matrix had to be created from the partial netmat information that is included in the HCP500 release. These are included as CIFTI files (.pconn.nii) which can be opened in HCP Workbench (specifically, in 'wb_view')
      - the specific files used were located in 
                    
            
            HCP_500_release/HCP500_Parcellation_Timeseries_Netmats/netmats_3T_Q1-Q6related468_MSMsulc_ICAd200_ts2.tar.gz
           
            
         _once you extract this file, a folder called 'netmats' is created, the actual CIFTI files needed are located in:_
            
            HCP_500_release/HCP500_Parcellation_Timeseries_Netmats/netmats/3T_Q1-Q6related468_MSMsulc_d200_ts2_netmat2
            
       - because the data is supplied as CIFTI files, HCP workbench's wb_command tool is used to convert them to .csv files
                
            _NOTE: There is a script included in this repo to accompish this, see "get_matrices.sh"_
                
   - after generating the CSV files with 200x200 node edge weight data, a python script was used to generate a CSV text file (called 'NET.txt') containing the 460x199000 matrix, to be fed into CCA as in Smith et al.

2. The subject-measure matrix was created using the rfMRI and quarter/release data on the [HCP-CCA site](https://www.fmrib.ox.ac.uk/datasets/HCP-CCA/), the restricted and behavioral (unrestricted) datasets from HCP, and the list of subjectIDs and subject measures provided on that site
   - The resulting matrix was 460x478 (460 subjects, 478 subject measures as listed in the column_headers.txt file on the HCP-CCA site) and outputted to a CSV text file ('vars.txt')
3. The analysis was re-run using the provided hcp_cca.m [code](https://www.fmrib.ox.ac.uk/datasets/HCP-CCA/hcp_cca.m)
   - the following data was used:
      - the NET.txt file
      - the vars.txt file
      - the unrestricted data currently available from the HCP 1200 release (it contains info on 1207 subjects)
      - the restricted data currently available from the HCP 1200 release (contains info on 1207 subjects)
      - the varsQconf file provided on the [HCP-CCA site](https://www.fmrib.ox.ac.uk/datasets/HCP-CCA/)
      - the rfMRI_motion.txt file provided on [HCP-CCA site](https://www.fmrib.ox.ac.uk/datasets/HCP-CCA/)
      - the quarter/release data provided on [HCP-CCA site](https://www.fmrib.ox.ac.uk/datasets/HCP-CCA/)
   
   - the analysis ran successfully, resulting in the following plot of the subject measure CCA weights vs. connectome CCA weights:
   
                    
                    
                            

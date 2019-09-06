# Human Connectome Project, CCA Analyses

## GOALS
The purpose of this analysis is to:

    * (1) Replicate the results of Smith et al. (https://www.fmrib.ox.ac.uk/datasets/HCP-CCA/)
    
    * (2) Run this analysis on the larger HCP 1200 patient dataset
    
    * (3) Create a clean, simple to use pipeline so others can replicate our analysis
    
    * (4) Expand this analysis to other connectome datasets
    
    
## DOCUMENTATION
The following documentation explains the entire process used to achieve Goal #1
**1.** Attempting to replicate Smith et al.
    **a.** Multiple datasets were acquired (see link https://www.fmrib.ox.ac.uk/datasets/HCP-CCA/ for more info)
        **i.** The subjects x partial connectome data (for example, in the HCP 500 set this would be a 460x19900 matrix of connectome edge weights for all subjects)
            **ia.** this matrix had to be generated from the partial netmat information that is included in the HCP500 release. These are included as CIFTI files (.pconn.nii) which can be opened in HCP Workbench (specifically, in 'wb_view')
            **ib.** the specific files used in our replication were located in: 
                    
            '''
            HCP_500_release/HCP500_Parcellation_Timeseries_Netmats/netmats_3T_Q1-Q6related468_MSMsulc_ICAd200_ts2.tar.gz
            '''
            **NOTE:** once you extract this file, a folder called 'netmats' is created, the actual CIFTI files needed are located in:
            '''
            HCP_500_release/HCP500_Parcellation_Timeseries_Netmats/netmats/3T_Q1-Q6related468_MSMsulc_d200_ts2_netmat2
            '''
            ic. because the data is supplied as CIFTI files, HCP workbench's wb_command tool is used to convert them to .csv files
                
                **NOTE: There is a script included in this repo to accompish this, see "get_matrices.sh"
                
            id. after generating the CSV files, you need to use the python script _________ to generate a NET.txt file, 
            which contains the subject x connectome data
            
                **NOTE: for replicating the Smith et al., this matrix will be 460x199900, because there are 460 subjects 
                in the release, and ICA with 200 components was used to generate the CIFTI files
            
            ie.
                    
                    
                            
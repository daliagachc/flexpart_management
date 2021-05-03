diego.aliaga at helsinki dot fi

## 2021-04-08_14-00-16_
- ignore la paz stuff. it should live here
- export folder is here: flexpart_management/releases/v03

- main export is this 
    - flexpart_management/notebooks/release_ds_v3/release_ds_v3_save_mega_ds.py
        - function get_dcc()
            - needs 
                 - ds_clustered_18_agl.nc
                    - created here:
                    [six_clusters_centroids_create_18agl.py](
                    flexpart_management/notebooks/six_clusters_centroids/six_clusters_centroids_create_18agl.py)
                    - needs ds_clustered_18.nc
                        - created here: [00_pre_clustering.py](
                        flexpart_management/notebooks/run_2019-10-02_13-42-52_/clustering/00_pre_clustering.py)
                    - needs 'prop_df_.csv'
                        - created here [06_cluster_properties.py](
                        flexpart_management/notebooks/run_2019-10-02_13-42-52_/clustering/06_cluster_properties.py)
                    
                    - needs 'nc_18_nc_06.csv'
                         - this one was made manually 
                 - 'new_log_pol_ds_agl.nc'
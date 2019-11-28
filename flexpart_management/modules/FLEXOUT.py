# project name: flexpart_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
"""class created to control the output from flexpart"""
from useful_scit.imps import *
import typing
import flexpart_management.modules.constants as co
import flexpart_management.modules.flx_array as fa
import pandas as pd

from flexpart_management.modules.flx_array import \
    get_and_tune_flexout_from_ds_and_head


class FLEXOUT :
    """
    class used to transform rect coords into polar coords.
    there should by a 'heads' folder inside the folder path:
    - folder path
        - file1.nc
        - file2.nc
        - heads
            - head.nc

    """
    dom: str = None
    folder_path: str = None
    head_file_path: str = None
    out_file_list: typing.List[ str ] = None
    head_ds: xr.Dataset = None
    out_ds_list: typing.List[ xr.Dataset ] = None
    head_pat: str = 'header_'
    out_file_pat: str = 'flxout_'
    out_path_pat: str = None
    out_dask_ds: xr.Dataset = None
    flexout_ds: xr.Dataset = None
    flexout_hour_ds_list: typing.List[ xr.Dataset ] = None
    flexout_hour_ds: xr.Dataset = None
    hours = 96
    folder_path_out: str = None
    run_name: str = None

    def __init__( self ,
                  dom: str ,
                  folder_path: str ,
                  folder_path_out: str = None ,
                  run_name: str = None ,
                  process: bool = True ,
                  export_log_pol: bool = False
                  ) :
        """
        create the object to transform from rect coords to polar coords.

        Parameters
        ----------
        dom
            d01 or d02
        folder_path
            where to find the files
        folder_path_out
            where to save the files
        run_name
            used as an id
        process
            for debug purposes: chose false if you want to process manually.
            set to true for compatibility
        export_log_pol
            same as above. set to false for compatibility
        """
        self.dom = dom

        # make sure you have a trailing /
        self.folder_path = os.path.join( folder_path , '' )
        self.folder_path_out = os.path.join( folder_path_out , '' )
        self.run_name = run_name

        self.head_file_path = self.set_head_path(
            folder_path=self.folder_path ,
            head_pat=self.head_pat ,
            dom=self.dom ,
            )

        if process :
            self.flexout_hour_ds = self.process_log_coords()

        if export_log_pol :
            self.export_log_polar_coords( keep_z=True )

    def process_log_coords( self ) -> xr.Dataset :
        self.out_path_pat , \
        self.out_file_list = self.set_out_file_path_list()
        self.out_file_list = self.check_files_are_not_corrupted()
        self.head_ds = xr.open_dataset( self.head_file_path )

        self.out_dask_ds = xr.open_mfdataset( self.out_file_list ,
                                              concat_dim=co.TIME ,
                                              combine='nested' , )

        self.out_dask_ds = fa.convert_ds_time_format( self.out_dask_ds )

        # add lat lot z vol alt etc
        self.flexout_ds = self.get_and_tune_flexout_ds(
            self.out_dask_ds ,
            self.head_ds ,
            )

        self.flexout_hour_ds_list = self.get_flx_hour_ds_list()
        # noinspection PyTypeChecker
        return xr.concat( self.flexout_hour_ds_list , dim=co.RL )

    import typing
    def get_flx_hour_ds_list( self ) -> typing.List[ xr.Dataset ] :
        releases = self.flexout_ds[ co.RL ]
        flexout_hour_ds_list = [ ]
        for r in releases :
            nds = self.flexout_ds.sel( **{ co.RL : r } )
            nds = fa.trim_swap_dim_coord( nds , self.hours )
            flexout_hour_ds_list.append( nds )
        return flexout_hour_ds_list

    @staticmethod
    def get_and_tune_flexout_ds( out_dask_ds , head_ds ) :
        return get_and_tune_flexout_from_ds_and_head( out_dask_ds , head_ds )

    @staticmethod
    def set_head_path( folder_path ,
                       head_pat ,
                       dom ,
                       ) :
        head_file = folder_path + '*' + head_pat + '*' + dom + '*'
        log.ger.debug( f'head file is {head_file}' )
        head_file = glob.glob( head_file )[ 0 ]
        log.ger.debug( f'head file again is {head_file}' )
        return head_file

    def set_out_file_path_list( self ) :
        out_path = self.folder_path + '*' + self.out_file_pat + '*' + \
                   self.dom + '*'
        log.ger.debug( f'out path is {out_path}' )
        out_path_list = glob.glob( out_path )
        out_path_list.sort()
        log.ger.debug( f'out path list 1st elemnt is {out_path_list[ :1 ]}' )
        return out_path , out_path_list

    def check_files_are_not_corrupted( self ) :
        new_out_list = [ ]
        for f in self.out_file_list :
            # noinspection PyBroadException
            try :
                # noinspection PyUnusedLocal
                nf = xr.open_dataset( f )
                new_out_list.append( f )
                log.ger.debug( f'file {f} opened' )
            except :
                # print('cant open', f)
                log.ger.error( f'file {f} is corrupted' )
        return new_out_list

    def get_log_polar_coords( self ,
                              release: pd.Timestamp ,
                              coords_to_keep=None ,
                              rounding_vals=None ,
                              keep_list=None
                              ) :
        if keep_list is None :
            keep_list = [ co.RL ]
        if coords_to_keep is None :
            coords_to_keep = [ co.WE , co.SN ]
        if rounding_vals is None :
            rounding_vals = [ co.ROUND_R_LOG ,
                              co.ROUND_TH_RAD ]

        keep_vars = [ co.CONC ]
        keep_coords = coords_to_keep

        sum_ds = self.flexout_hour_ds
        sum_ds = sum_ds[ keep_vars ].sel( **{ co.RL : release } )
        complement_coords = fa.get_dims_complement( sum_ds , keep_coords )
        log.ger.debug( 'completemt coords: %s' , complement_coords )
        sum_ds = sum_ds.sum( dim=complement_coords )

        # log.ger.debug(sum_ds)

        val = rounding_vals
        log_pol_ds = xr.Dataset()
        for v in keep_vars :
            log_pol_ds[ v ] = fa.data_array_to_logpolar( da=sum_ds[ v ] ,
                                                    dim2keep=keep_list ,
                                                    r_round_log=val[ 0 ] ,
                                                    th_round_rad=val[ 1 ] )

        return log_pol_ds

    def export_log_polar_coords( self , keep_z=False ) -> None :
        """
        read and export the log polar coords to a file
        Parameters
        ----------
        keep_z:bool
            keep the z information

        Returns
        -------

        """
        release_name = 'release_name'
        release_path = 'release_path'
        coords_to_keep = [ co.WE , co.SN ]
        rounding_vals = [ co.ROUND_R_LOG , co.ROUND_TH_RAD ]
        keep_list = [ co.RL ]

        if keep_z :
            coords_to_keep = [ co.WE , co.SN , co.BT ]
            keep_list = [ co.RL , co.ZT ]

        out_path = os.path.join( self.folder_path_out , self.run_name )
        os.makedirs( out_path , exist_ok=True )

        releases = self.flexout_hour_ds[ co.RL ]
        release_df = self.get_release_df( release_name , release_path ,
                                          releases , out_path )
        conc_path_out = release_df.iloc[ 0 ][ release_path ]

        # noinspection PyBroadException
        log_pol_exists = self._check_log_pol_file_exists( conc_path_out )

        if log_pol_exists is False :
            list_log_polar_ds = [ ]
            for key , row in release_df[ : ].iterrows() :
                # noinspection PyBroadException
                try :
                    log_pol_ds = self.get_log_polar_coords(
                        release=row[ co.RL ] ,
                        coords_to_keep=coords_to_keep ,
                        rounding_vals=rounding_vals ,
                        keep_list=keep_list
                        )
                    # fa.compressed_netcdf_save(log_pol_ds,row[release_path])
                    list_log_polar_ds.append( log_pol_ds )
                    # print('done getting polar coords',k)
                    log.ger.debug( f'done getting coords' )
                except :
                    # print('error in',k)
                    log.ger.error( f'error in {key}' )

            conc_ds = xr.concat( list_log_polar_ds , dim=co.RL )
            log.ger.debug( 'save path %s' , conc_path_out )
            log.ger.debug( 'length arr %s' , len( list_log_polar_ds ) )
            fa.compressed_netcdf_save( conc_ds , conc_path_out )

    def _check_log_pol_file_exists( self , conc_path_out ) :
        try :
            # lets try to see if the file exists and can be opened
            log_pol_ds = xr.open_dataset( conc_path_out )
            log_pol_ds.close()
            log.ger.debug( f'log_pol_file exists' )
            log_pol_exists = True
        except :
            log.ger.debug( f'''
            log pol file doesnt exist. creating a new one. 
            ''' )
            log_pol_exists = False
        return log_pol_exists

    def get_release_df( self , releas_name , release_path , releases ,
                        out_path ) :
        release_df = releases.to_dataframe()
        release_df[ releas_name ] = release_df[ co.RL ].dt.strftime(
            self.dom + '_%Y-%m-%d_%H-%M-%S.nc' )
        release_df[ release_path ] = release_df[ releas_name ].apply(
            lambda n : os.path.join( out_path , n ) )
        return release_df

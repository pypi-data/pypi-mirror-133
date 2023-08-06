"""
modxlib - Utilites used by CTPS Model Data Explorer for TDM23.

The uilities fall into the following categories:
0. Version identification
1. Trip Table management
2. TAZ "shapefile" management
3. Utilities for the transit mode
4. Utilities for working with highway assignment data
5. Utilities for working with "skims"
6. Utilities for working with dataframes and geodataframes

This list will be continued.
"""
# modxlib23.py - Python module implementing CTPS 'modxlib23'
#
# Author: Ben Krepp (bkrepp@ctps.org)
#

import csv
import numpy as np
import pandas as pd
import geopandas as gp
from dbfread import DBF
import pydash

###############################################################################
#
# Section 0: Version identification
#
_version = "0.2.1"
def get_version():
    return _version
# end_def


###############################################################################
#
# Section 1: Trip table management
#
class TripTableMgr():
    """ 
    Class for trip table utilities
    """
    _veh_modes = [ 'sov', 'hov', 'ltrk', 'mtrk', 'htrk' ]
    _per_modes = [ 'auto', 'nonm', 'ta_acc', 'ta_egr', 'tw' ]
    _all_modes = _veh_modes + _per_modes
    
    def __init__(self):
        pass
    #
    
    def open_trip_tables(self, scenario_dir):
        """
        Function: open_trip_tables - TDM23 implementation

        Summary: Given a directory containing the trip tables in OMX format for the 
                 four daily time periods used by the TDM23 model, open them and return 
                 a dictionary with a two-level dictionary structure: the first level of which
                 is { 'veh', 'per' }, and the second of which are the four time periods
                {'am', 'md', 'pm', 'nt'}. The 'leaf' value of each element of this 2-level
                dictionary is the corresponding open OMX file.

        Args: scenario_dir: directory containing TDM23 output for a given scenario;
              the OMX-format trip-tables are found in the '_summary' subdirectory

        Returns: A two-level dictionary structure: the first level of which
                 is the four time periods {'am', 'md', 'pm', 'nt'}, and the
                 second of which is ( 'veh', 'per' ).
                .The 'leaf' value of each element of this 2-level dict
                 is the corresponding open OMX file.
                 
        Raises: N/A
        """
        tt_dir = scenario_dir + '/_summary/'
        tt_am_veh = tt_dir + 'od_veh_am.omx'
        tt_am_per = tt_dir + 'od_per_am.omx'
        tt_md_veh = tt_dir + 'od_veh_md.omx'
        tt_md_per = tt_dir + 'od_per_md.omx'
        tt_pm_veh = tt_dir + 'od_veh_pm.omx'
        tt_pm_veh = tt_dir + 'od_per_pm.omx'
        tt_nt_veh = tt_dir + 'od_veh_nt.omx'
        tt_nt_per = tt_dir + 'od_per_nt.omx'
        tt_omxs =   { 'am' : { 'veh' : omx.open_file(tt_am_veh,'r'),
                               'per' : omx.open_file(tt_am_per,'r') },
                      'md' : { 'veh' : omx.open_file(tt_md_veh,'r'),
                               'per' : omx.open_file(tt_md_per,'r') },
                      'pm' : { 'veh' : omx.open_file(tt_pm_veh,'r'),
                               'per' : omx.open_file(tt_pm_per,'r') },
                      'nt' : { 'veh' : omx.open_file(tt_nt_veh,'r'),
                               'per' : omx.open_file(tt_nt_per,'r') }
                    }
        return tt_omxs
    #
    #
    def load_trip_tables(tt_omxs, veh_modes=None, per_modes=None):
        """
        Function: load_trip_tables - TDM123 implementation

        Summary: Load the trip tables for all time periods the specified list of modes from
                 the OMX files dict returned by openn_trip_tables into NumPy arrays.
                 If no list of modes is passed, trip tables for all modes will be returned.

        Args: tt_omxs: Dictionary, keyed by time period identifier ('am', 'md', 'pm', and 'nt'),
                       each of whose values is the open OMX trip table file for the corresponding
                       time period.
               modes: List of modes (strings) or None

        Returns: A two-level dictionary (i.e., first level = time period, second level = mode)
                 the second level of which contain the trip table, in the form of a numPy array,
                 for the [time_period][mode] in question.

        Raises: N/A
        """
        if veh_modes == None:
            veh_modes = self._veh_modes
        #
        if per_modes == None:
            per_modes = self._per_modes
        #
        retval  = { 'am' : {}, 'md' : {}, 'pm' : {}, 'nt' : {} }
        for period in self._all_time_periods:
            for mode in veh_modes:
                temp = tt_omxs[period]['veh'][mode]
                retval[period][mode] = np.array(temp)
            # end_for
            for mode in per_modes:
                temp = tt_omxs[period]['per'][mode]
                retval[period][mode] = np.array(temp)
            # end_for
        # end_for
        return retval
    #
# class TripTableMgr


###############################################################################
#
# Section 2: TAZ "shapefile" management
#
#
class TazManager():
    """
    class: TazManager

    Summary: The class "TazManager" provides a set of methods to perform _attribute_ queries
             on an ESRI-format "Shapefile" that represents the TAZes in the model region.
             The attributes are read from the Shapefile's .DBF file; other components of
             the Shapefile are ignored.
             
    The Shapefile's .DBF file _must_ contain the following attributes:
    1. id
    2. taz
    3. type - 'I' (internal) or 'E' (external)
    4. town
    5. state - state abbreviation, e.g., 'MA'
    6. town_state - town, state
    7. mpo - abbreviation of MPO name: 
    8. in_brmpo - 1 (yes) or 0 (no)
    9. subregion - abbreviation of Boston Region MPO subregion or NULL
    10. sector - 'analysis sector' as defined by Bill Kuttner.
                  Either 'Northeast', 'North', 'Northwest', 'West', 'Southwest',
                  'South', 'Southeast', 'Central' or ''; the empty string ('')
                  indicates that the TAZ is outsize of the 164 municipalities
                  comprising what was once known as the 'CTPS Model Region'.

    An object of class TazManager is instantiated by passing in the fully-qualified path
    to a Shapefile to the class constructor. Hence, it is possible to have more than one
    instance of this class active simultaneously, should this be needed.

    Note: For all of the above methods listed bleo that return a "list of TAZ records", 
    each returned 'TAZ' is a Python 'dict' containing all of the keys (i.e., 'attributes') listed above. 
    To convert such a list to a list of _only_ the TAZ IDs, call taz_ids on the list of TAZ records.
    """
    _instance = None
    _default_shapefile_dir = r'G:/Data_Resources/modx/canonical_TAZ_shapefile/'
    _default_shapefile_fn = 'candidate_CTPS_TAZ_STATEWIDE_2019.shp'
    # _default_fq_shapefile_fn = _default_base + _default_shapefile_fn
    _taz_table = []
    
    def __init__(self, my_shapefile_dir=None, my_shapefile_fn=None):
        # print('Creating the TazManager object.')
        if my_shapefile_dir == None:
            my_shapefile_dir = self._default_shapefile_dir
        if my_shapefile_fn == None:
            my_shapefile_fn = self._default_shapefile_fn
        #
        my_shapefile_fq_fn = my_shapefile_dir + my_shapefile_fn
        # Derive name of .dbf file 
        my_dbffile_fn = my_shapefile_fq_fn.replace('.shp', '.dbf')
        dbf_table = DBF(my_dbffile_fn, load=True)
        for record in dbf_table.records:
            new = {}
            new['id'] = int(record['id'])
            new['taz'] = int(record['taz'])
            new['type'] = record['type']
            new['town'] = record['town']
            new['state'] = record['state']
            new['town_state'] = record['town_state']
            new['mpo'] = record['mpo']
            new['in_brmpo'] = int(record['in_brmpo'])
            new['subregion'] = record['subregion']
            new['sector'] = record['sector']
            self._taz_table.append(new)
        # end_for
        dbf_table.unload()
        print('Number of records read = ' + str(len(self._taz_table)))
        return self._instance
    # end_def __init__()
    
    # For debugging during development:
    def _get_tt_item(self, index):
        return self._taz_table[index]
      
    def mpo_to_tazes(self, mpo):
        """
        mpo_to_tazes(mpo): Given the name (i.e., abbreviation) of an MPO,
                           return a list of the records for the TAZes in it
        """
        retval = pydash.collections.filter_(self._taz_table, lambda x: x['mpo'] == mpo)
        return retval
    
    def brmpo_tazes(self):
        """
        brmpo_tazes(self) - Return the list of the records for the TAZes in the Boston Region MPO
        """
        retval = pydash.collections.filter_(self._taz_table, lambda x: x['in_brmpo'] == 1)
        return retval
    
    def brmpo_town_to_tazes(self, mpo_town):
        """
        brmpo_town_to_tazes(town) - Given the name of a town in the Boston Region MPO,
                                    return a list of the records for the TAZes in it
        """
        retval = pydash.collections.filter_(self._taz_table, lambda x: x['in_brmpo'] == 1 and x['town'] == mpo_town)
        return retval
    
    def brmpo_subregion_to_tazes(self, mpo_subregion):
        """
        brmpo_subregion_to_tazes(subregion) - Given the name (i.e., abbreviation) of a Boston Region MPO subregion,
                                              return a list of the records for the TAZes in it
        """
        # We have to be careful as some towns are in two subregions,
        # and for these the 'subregion' field of the table contains
        # an entry of the form 'SUBREGION_1/SUBREGION_2'.
        retval = []
        if subregion == 'ICC':
            retval = pydash.collections.filter_(self._taz_table, 
                                                lambda x: x['subregion'].find('ICC') != -1)
        elif subregion == 'TRIC':
            retval = pydash.collections.filter_(self._taz_table, 
                                                lambda x: x['subregion'].find('TRIC') != -1)
        elif subregion == 'SWAP':
            retval = pydash.collections.filter_(self._taz_table,
                                                lambda x: x['subregion'].find('SWAP') != -1)
        else:
            retval = pydash.collections.filter_(self._taz_table, lambda x: x['subregion'] == mpo_subregion)
        # end_if
        return retval
    # end_def mpo_subregion_to_tazes()
     
    def sector_to_tazes(self, sector):
        """
        sector_to_tazes - Given the name of an 'analysis sector', return the list of the records for the TAZes
                          in the sector.
        """
        retval = pydash.collections.filter_(self._taz_table, lambda x: x['sector'] == sector)
        return retval
        
    # Note: Returns TAZes in town _regardless_ of state.
    def town_to_tazes(self, town):
        """
         town_to_tazes(town) - Given the name of a town, return the list of the records for the TAZes in the town.
                               Note: If a town with the same name occurs in more than one state, the  list of TAZes
                               in _all_ such states is returned.
        """
        retval = pydash.collections.filter_(self._taz_table, lambda x: x['town'] == town)
        return retval
    
    def town_state_to_tazes(self, town, state):
        """
        town_state_to_tazes(town, state) - Given a town and a state abbreviation (e.g., 'MA'),
                                           return the list of records for the TAZes in the town.
        """
        retval = pydash.collections.filter_(self._taz_table, lambda x: x['state'] == state and x['town'] == town)
        return retval
    
    def state_to_tazes(self, state):
        """
        state_to_tazes(state) - Given a state abbreviation, return the list of records for the TAZes in the state.
        """
        retval = pydash.collections.filter_(self._taz_table, lambda x: x['state'] == state)
        return retval
            
    def taz_ids(self, taz_record_list):
        """
        taz_ids(TAZ_record_list) - Given a list of TAZ records, return a list of _only_ the TAZ IDs from those records.
        """
        retval = []
        for taz in taz_record_list:
            retval.append(taz['id'])
        # end_for
        return retval
    #
# end_class TazManager


###############################################################################
#
# Section 3: Miscellaneous utilities for the transit mode
#

# The following function "should" be applicable to TDM23. (It was to TDM19.)
# This is currently to be determined.
def calculate_total_daily_boardings(boardings_by_tod):
    """
    Function: calculate_total_daily_boardings
    
    Summary: Calculate the daily total boardings across all time periods.
    This calculation requires a bit of subtelty, because the number of rows in the four
    data frames produced by produced in the calling function is NOT necessarily the same. 
    A brute-force apporach will not work, generally speaking.
    See comments in the code below for details.
    
    NOTE: This is a helper function for import_transit_assignment, which see.
    
    Args: boardings_by_tod: a dict with the keys 'AM', 'MD', 'PM', and 'NT'
          for which the value of each key is a data frame containing the total
          boardings for the list of routes specified in the input CSV file.
    
    Returns: The input dict (boardings_by_tod) with an additional key 'daily'
             the value of which is a dataframe with the total daily boardings
             for all routes specified in the input CSV across all 4 time periods.
    
    Raises: N/A
    """
    am_results = boardings_by_tod['AM']
    md_results = boardings_by_tod['MD']
    pm_results = boardings_by_tod['PM']
    nt_results = boardings_by_tod['NT']
    #
    # Compute the daily sums.
    #
    # Step 1: Join 'am' and 'md' dataframes
    j1 = pd.merge(am_results, md_results, on=['ROUTE', 'STOP'], how='outer', suffixes=('_am', '_md'))
    # Step 1.1 Replace NaN's with 0's
    j1 = j1.fillna(0)
    #
    # Step 1.2 Compute the 'AM' + 'MD' sums
    j1['DirectTransferOff'] = j1['DirectTransferOff_am'] + j1['DirectTransferOff_md']
    j1['DirectTransferOn'] = j1['DirectTransferOn_am'] + j1['DirectTransferOn_md']
    j1['DriveAccessOn'] = j1['DriveAccessOn_am'] + j1['DriveAccessOn_md']
    j1['EgressOff'] = j1['EgressOff_am'] + j1['EgressOff_md']
    j1['Off'] = j1['Off_am'] + j1['Off_md']
    j1['On'] = j1['On_am'] + j1['On_md']
    j1['WalkAccessOn'] = j1['WalkAccessOn_am'] + j1['WalkAccessOn_md'] 
    j1['WalkTransferOff'] = j1['WalkTransferOff_am'] + j1['WalkTransferOff_md']
    j1['WalkTransferOn'] = j1['WalkTransferOn_am'] + j1['WalkTransferOn_md']
    #
    # Step 1.3: Drop un-needed columns
    cols_to_drop = ['DirectTransferOff_am', 'DirectTransferOff_md',
                    'DirectTransferOn_am', 'DirectTransferOn_md',
                    'DriveAccessOn_am', 'DriveAccessOn_md',
                    'EgressOff_am','EgressOff_md',
                    'Off_am', 'Off_md',
                    'On_am', 'On_md',
                    'WalkAccessOn_am', 'WalkAccessOn_md',
                    'WalkTransferOff_am', 'WalkTransferOff_md',
                    'WalkTransferOn_am', 'WalkTransferOn_md']
    #
    j1 = j1.drop(columns=cols_to_drop)
    #
    # Step 2: j2 - join 'pm' and 'nt' data frames
    j2 = pd.merge(pm_results, nt_results, on=['ROUTE', 'STOP'], how='outer', suffixes=('_pm', '_nt'))
    # Step 2.1: Replace NaN's with 0's
    j2 = j2.fillna(0)
    #
    # Step 2.2: Compute the 'PM' + 'NT' sums
    j2['DirectTransferOff'] = j2['DirectTransferOff_pm'] + j2['DirectTransferOff_nt']
    j2['DirectTransferOn'] = j2['DirectTransferOn_pm'] + j2['DirectTransferOn_nt']
    j2['DriveAccessOn'] = j2['DriveAccessOn_pm'] + j2['DriveAccessOn_nt']
    j2['EgressOff'] = j2['EgressOff_pm'] + j2['EgressOff_nt']
    j2['Off'] = j2['Off_pm'] + j2['Off_nt']
    j2['On'] = j2['On_pm'] + j2['On_nt']
    j2['WalkAccessOn'] = j2['WalkAccessOn_pm'] + j2['WalkAccessOn_nt'] 
    j2['WalkTransferOff'] = j2['WalkTransferOff_pm'] + j2['WalkTransferOff_nt']
    j2['WalkTransferOn'] = j2['WalkTransferOn_pm'] + j2['WalkTransferOn_nt']
    #
    # Step 2.3: Drop un-needed columns
    cols_to_drop = ['DirectTransferOff_pm', 'DirectTransferOff_nt',
                    'DirectTransferOn_pm', 'DirectTransferOn_nt',
                    'DriveAccessOn_pm', 'DriveAccessOn_nt',
                    'EgressOff_pm','EgressOff_nt',
                    'Off_pm', 'Off_nt',
                    'On_pm', 'On_nt',
                    'WalkAccessOn_pm', 'WalkAccessOn_nt',
                    'WalkTransferOff_pm', 'WalkTransferOff_nt',
                    'WalkTransferOn_pm', 'WalkTransferOn_nt'
                    ]
    j2 = j2.drop(columns=cols_to_drop)
    #
    # Step 3: Join "j1" and "j2" to produce a dataframe with the daily totals
    daily_df = pd.merge(j1, j2, on=['ROUTE', 'STOP'], how='outer', suffixes=('_j1', '_j2'))
    # Step 3.1 : Replace any NaN's with 0's. This line _shouldn't_ be needed - just being extra cautious.
    daily_df = daily_df.fillna(0)
    #
    # Step 3.2 : Compute THE daily sums
    daily_df['DirectTransferOff'] = daily_df['DirectTransferOff_j1'] + daily_df['DirectTransferOff_j2']
    daily_df['DirectTransferOn'] = daily_df['DirectTransferOn_j1'] + daily_df['DirectTransferOn_j2']
    daily_df['DriveAccessOn'] = daily_df['DriveAccessOn_j1'] + daily_df['DriveAccessOn_j2']
    daily_df['EgressOff'] = daily_df['EgressOff_j1'] + daily_df['EgressOff_j2']
    daily_df['Off'] = daily_df['Off_j1'] + daily_df['Off_j2']
    daily_df['On'] = daily_df['On_j1'] + daily_df['On_j2']
    daily_df['WalkAccessOn'] = daily_df['WalkAccessOn_j1'] + daily_df['WalkAccessOn_j2'] 
    daily_df['WalkTransferOff'] = daily_df['WalkTransferOff_j1'] + daily_df['WalkTransferOff_j2']
    daily_df['WalkTransferOn'] = daily_df['WalkTransferOn_j1'] + daily_df['WalkTransferOn_j2']
    #
    # Step 3.3 : Drop un-needed columns
    cols_to_drop = ['DirectTransferOff_j1', 'DirectTransferOff_j2',
                    'DirectTransferOn_j1', 'DirectTransferOn_j2',
                    'DriveAccessOn_j1', 'DriveAccessOn_j2',
                    'EgressOff_j1','EgressOff_j2',
                    'Off_j1', 'Off_j2',
                    'On_j1', 'On_j2',
                    'WalkAccessOn_j1', 'WalkAccessOn_j2',
                    'WalkTransferOff_j1', 'WalkTransferOff_j2',
                    'WalkTransferOn_j1', 'WalkTransferOn_j2'
                    ]
    daily_df = daily_df.drop(columns=cols_to_drop)
    #
    # Finally, we've got the 'daily' total dataframe!
    boardings_by_tod['daily'] = daily_df
    return boardings_by_tod
# end_def calculate_total_daily_boardings()

# The following function "should" be applicable to TDM23. (It was to TDM19.)
# This is currently to be determined.
def import_transit_assignment(scenario):
    """
    Function: import_transit_assignment
    
    NOTE: This method _should_ work equally well for TDM19 and TDM23.
          Under TDM19, the directory containing the output CSVs may (and often did)
          contain multiple CSVs per mode; under TMD23, it will contain only one CSV
          file per mode. The code will work equally well in both cases.
          For TDM23, some change to the location of the directory containing the 
          CSV files may be required.
    
    Summary:  Import transit assignment result CSV files for a given scenario.
    
    1. Read all CSV files for each time period ('tod'), and caclculate the sums for each time period.
       Step 1 can be performed as a brute-force sum across all columns, since the number of rows in
       the CSVs (and thus the dataframes) for any given time period are all the same.
    
    2. Calculate the daily total across all time periods.
       Step 2 requires a bit of subtelty, because the number of rows in the data frames produced in 
       Step 1 is NOT necessarily the same. A brute-force apporach will not work, generally speaking.
       See comments in the code below for details.
       NOTE: This step is performed by the helper function calculate_total_daily_boardings.
    
    Args: scenario: path to directory containing transit assignment results in CSV file format
    
    Returns: a dict of the form:
            { 'AM'    : dataframe with totals for the AM period,
              'MD'    : datafrme with totals for the MD period,
              'PM'    : dataframe with totals for the PM period,
              'NT'    : dataframe with totals for the NT period,
              'daily' : dataframe with totals for the entire day
            }
    
    Raises: N/A
    """
    base = scenario + r'out/'
    tods = ["AM", "MD", "PM", "NT"]
    # At the end of execution of this function, the dictionary variable'TODsums' will contain all the TOD summed results:
    # one key-value-pair for each 'tod' AND the 'daily' total as well.
    #
    # The dict 'TODsums' is the return value of this function.
    TODsums = { 'AM' : None, 'MD' : None, 'PM' : None, 'NT' : None }
    #
    # Import CSV files and create sum tables for each T-O-D (a.k.a. 'time period').
    for tod in tods:
        # Get full paths to _all_ CSV files for the current t-o-d.
        x = tod + '/' 
        fq_csv_fns = glob.glob(os.path.join(base,x,r'*.csv'))
        #      
        # 'tablist' : List of all the dataframes created from reading in the all the CSV files for the current t-o-d
        tablist = []
        for csv_file in fq_csv_fns:
            # Read CSV file into dataframe, set indices, and append to 'tablist'
            tablist.append(pd.read_csv(csv_file).set_index(['ROUTE','STOP']))
        #
        # Sum the tables for the current TOD
        TODsums[tod] = reduce(lambda a, b: a.add(b, fill_value=0), tablist)
    # end_for over all tod's
    #
    TODsums =  calculate_total_daily_boardings(TODsums)
    #
    # Ensure that the ROUTE and STOP columns of each dataframe in TODsums aren't indices.
    for k in TODsums.keys():
        TODsums[k] = TODsums[k].reset_index()
    #
    return TODsums
# end_def import_transit_assignment()
#
# END of Section 3: Utilities for the transit mode
###############################################################################


###############################################################################
#
# Section 4: Utilities for the highway mode
#
class HighwayAssignmentMgr():
    """ 
    Class for highway assignment utilities
    """
    
    def __init__(self):
        pass
    #
    
    _hwy_asgn_columns = [ 'ID', 'Anode', 'Bnode', 'Length', 
                        'street_name', 'route_number', 'taz_id', 'dir', 'func_class', 
                        'AB_lanes', 'BA_lanes', 
                        'shoulder_am', 'shoulder_pm', 
                        'AB_off_am', 'BA_off_am', 
                        'AB_off_pm', 'BA_off_pm', 
                        'peak_hov', 'max_truck_size',
                        'toll_auto', 'toll_lt_trk', 'toll_md_trk', 'toll_hv_trk', 
                        'posted_speed', 'median', 'area_type', 'access_control', 
                        'alpha_input', 'beta_input', 'ff_speed_input', 'capacity_input',
                        'auto_time_input', 'transit_time_input', 'walk_time_input',
                        'pnr_parking_cost', 'pnr_shadow_cost_am_input', 'available', 
                        'project_name', 'project_id', 'count_station', 
                        'hov_only', 'truck_only',
                        'small_veh_only', 'no_heavy_truck', 'transit_only', 'walk_bike_only', 'no_walk_bike', 
                        'alpha', 'beta', 'ff_time', 'capacity',
                        'AB_AM_capacity', 'AB_MD_capacity', 'AB_PM_capacity', 'AB_NT_capacity',
                        'BA_AM_capacity', 'BA_MD_capacity', 'BA_PM_capacity', 'BA_NT_capacity',
                        'AB_AM_ctime', 'AB_MD_ctime', 'AB_PM_ctime', 'AB_NT_ctime',
                        'BA_AM_ctime', 'BA_MD_ctime', 'BA_PM_ctime', 'BA_NT_ctime',
                        'AB_AM_cspd', 'AB_MD_cspd', 'AB_PM_cspd', 'AB_NT_cspd',
                        'BA_AM_cspd', 'BA_MD_cspd', 'BA_PM_cspd', 'BA_NT_cspd',
                        'AB_AM_vol', 'AB_MD_vol', 'AB_PM_vol', 'AB_NT_vol',
                        'BA_AM_vol', 'BA_MD_vol', 'BA_PM_vol', 'BA_NT_vol',
                        'AB_AM_vmt', 'AB_MD_vmt', 'AB_PM_vmt', 'AB_NT_vmt',
                        'BA_AM_vmt', 'BA_MD_vmt', 'BA_PM_vmt', 'BA_NT_vmt',
                        'AB_AM_vht', 'AB_MD_vht', 'AB_PM_vht', 'AB_NT_vht',
                        'BA_AM_vht', 'BA_MD_vht', 'BA_PM_vht', 'BA_NT_vht',
                        'AB_AM_vht', 'AB_MD_vht', 'AB_PM_vht', 'AB_NT_vht',
                        'BA_AM_vht', 'BA_MD_vht', 'BA_PM_vht', 'BA_NT_vht',
                        'AB_AM_pce', 'AB_MD_pce', 'AB_PM_pce', 'AB_NT_pce',
                        'BA_AM_pce', 'BA_MD_pce', 'BA_PM_pce', 'BA_NT_pce',
                        'AB_AM_voc', 'AB_MD_voc', 'AB_PM_voc', 'AB_NT_voc',
                        'BA_AM_voc', 'BA_MD_voc', 'BA_PM_voc', 'BA_NT_voc',
                        'AB_AM_sov', 'AB_MD_sov', 'AB_PM_sov', 'AB_NT_sov',
                        'BA_AM_sov', 'BA_MD_sov', 'BA_PM_sov', 'BA_NT_sov',
                        'AB_AM_hov', 'AB_MD_hov', 'AB_PM_hov', 'AB_NT_hov',
                        'BA_AM_hov', 'BA_MD_hov', 'BA_PM_hov', 'BA_NT_hov',
                        'AB_AM_ltrk', 'AB_MD_ltrk', 'AB_PM_ltrk', 'AB_NT_ltrk',
                        'BA_AM_ltrk', 'BA_MD_ltrk', 'BA_PM_ltrk', 'BA_NT_ltrk',
                        'AB_AM_mtrk', 'AB_MD_mtrk', 'AB_PM_mtrk', 'AB_NT_mtrk',
                        'BA_AM_mtrk', 'BA_MD_mtrk', 'BA_PM_mtrk', 'BA_NT_mtrk',
                        'AB_AM_htrk', 'AB_MD_htrk', 'AB_PM_htrk', 'AB_NT_htrk',
                        'BA_AM_htrk', 'BA_MD_htrk', 'BA_PM_htrk', 'BA_NT_htrk',
                        'AB_daily_vol', 'BA_daily_vol', 'AB_daily_vmt', 'BA_daily_vmt', 'AB_daily_vht', 'BA_daily_vht',
                        'AB_daily_sov', 'BA_daily_sov', 'AB_daily_hov', 'BA_daily_hov',
                        'AB_daily_ltrk', 'AB_daily_ltrk', 'AB_daily_mtrk', 'BA_daily_mtrk', 'AB_daily_htrk', 'BA_daily_htrk' ]
    
    def load_highway_assignment(self, scenario, columns=None):
        """"
            Method: load_highway_assignment(self, scenario, columns=None)
                    load TDM23 highway assignment data in CSV format into 4 pandas dataframes
                    in a dictionary indexed by time period { 'am', 'md', 'pm', 'nt' }
                    
            Args:   scenario - root directory of TDM23 scenario output
                    columns - columns in the CSV files to load;
                              the default value (None) indicates loading all columns
            
            Returns: 4 pandas dataframes organized as a dict indexed by time period 
                     
            Raises: N/A
        """
        if columns == None:
            columns = self._hwy_asgn_columns
        #
        link_flow_dir = scenario_dir + '_demand/highway/'
        
        am_flow_fn = link_flow_dir + 'AM_MMA_LinkFlow.csv'
        md_flow_fn = link_flow_dir + 'MD_MMA_LinkFlow.csv'
        pm_flow_fn = link_flow_dir + 'PM_MMA_LinkFlow.csv'
        nt_flow_fn = link_flow_dir + 'NT_MMA_LinkFlow.csv'
        
        retval = { 'am' : pd.read_csv(am_flow_fn, delimiter=',', usecols=columns),
                   'md' : pd.read_csv(md_flow_fn, delimiter=',', usecols=columns),
                   'pm' : pd.read_csv(pm_flow_fn, delimiter=',', usecols=columns),
                   'nt' : pd.read_csv(nt_flow_fn, delimiter=',', usecols=columns),
        }
        return retval
    #
# class HighwayAssignmentMgr

###############################################################################
#
# Section 5: Utilities for working with "skims"
#
class SkimsMgr():
    """ 
    Class for managing "skims" data
    """
    
    _skim_periods = [ 'am', 'md' ]
    _highway_skim_matrices = [ 'da_time', 'da_toll', 'dist', 'sr_time', 'sr_toll' ]
    _walk_matrices = [ 'dist', 'walk_time' ]
    _bike_matrices = [ 'dist', 'bike_time' ]
    _transit_auto_skim_matrices = [ 'Fare', 'auto_cost', 'ddist', 'dtime', 'gen_cost', 
                                    'ivtt', 'iwait', 'tdist', 'walk' , 'xfer', 'xwait' ]
    _transit_walk_skim_matrices = [ 'Fare', 'gen_cost', 
                                'ivtt', 'iwait', 'tdist', 'walk' , 'xfer', 'xwait' ]
    
    def __init__(self):
        pass
    #
    def load_highway_skims(self, skims_dir, periods=_skim_periods, matrices=_highway_skim_matrices):
        """"
            Method: load_highway_skims(self, skims_dir, periods=_skim_periods, matrices=_highway_skim_matrices)
                    load TDM23 highway skims as numPy arrays into a 2-level dictionary:
                    the first level of which is time period, the second level of which is matrix name
                    
            Args:   skims_dir - root directory where TDM23 skim output can be found
                    period - list of time periods for which to read skims
                    matrices - list of skim matrices to read for each time period
            
            Returns: a 2-level dict containing the specified skim matrices as numPy arrays
                     
            Raises: N/A
        """
        retval = {  'am' : {    'da_time' : None,
                                'da_toll' : None,
                                'dist'    : None,
                                'sr_time' : None,
                                'sr_toll' : None
                            },
                    'md' : {    'da_time' : None,
                                'da_toll' : None,
                                'dist'    : None,
                                'sr_time' : None,
                                'sr_toll' : None
                            }
                }
        for period in periods:
            omxfn = skims_dir + r'\highway_skim_' + period + '.omx'
            skim_omx = omx.open_file(omxfn,'r')
            for matrix in matrices:
                retval[period][matrix] = skim_omx[matrix]
            # end inner for
        # end outer for
        return retval
    # end_def load_highway_skims
    
    def load_walk_skims(self, skims_dir, matrices=_walk_matrices):
        """"
            Method: load_walk_skims(self, skims_dir, matrices=_walk_skim_matrices)
                    load TDM23 transit-auto skims as numPy arrays into a dictionary
                    indexed by matrix name
            
            Args:   skims_dir - root directory where TDM23 skim output can be found
                    matrices - list of skim matrices to read
            
            Returns: a dict containing the specified skim matrices as numPy arrays
            
            Raises: N/A
        """
        retval = {  'dist'      : None,
                    'walk_time' : None
                }
        omxfn = skims_dir + r'\walk_skim_.omx'
        skim_omx = omx.open_file(omxfn,'r')
        for matrix in matrices:
            retval[matrix] = skim_omx[matrix]
        # end_for
        return retval
    # end_def
    
    def load_bike_skims(self, skims_dir, matrices=_bike_matrices):
        """"
            Method: load_bike_skims(self, skims_dir, matrices=_walk_skim_matrices)
                    load TDM23 transit-auto skims as numPy arrays into a dictionary
                    indexed by matrix name
            
            Args:   skims_dir - root directory where TDM23 skim output can be found
                    matrices - list of skim matrices to read
            
            Returns: a dict containing the specified skim matrices as numPy arrays
            
            Raises: N/A
        """
        retval = {  'dist'      : None,
                    'bike_time' : None
                }
        omxfn = skims_dir + r'\bike_skim_.omx'
        skim_omx = omx.open_file(omxfn,'r')
        for matrix in matrices:
            retval[matrix] = skim_omx[matrix]
        # end_for
        return retval
    # end_def
   
    def load_transit_auto_skims(self, skims_dir, periods=_skim_periods, matrices=_transit_auto_skim_matrices):
        """"
            Method: load_transit_auto_skims(self, skims_dir, periods=_skim_periods, matrices=_transit_auto_skim_matrices)
                    load TDM23 transit-auto skims as numPy arrays into a 2-level dictionary:
                    the first level of which is time period, the second level of which is matrix name
            
            Args:   skims_dir - root directory where TDM23 skim output can be found
                    period - list of time periods for which to read skims
                    matrices - list of skim matrices to read for each time period
            
            Returns: a 2-level dict containing the specified skim matrices as numPy arrays
            
            Raises: N/A
        """
        retval = {  'am' : {    'Fare'      : None,
                                'auto_cost' : None,
                                'ddist_dist': None,
                                'dtime'     : None,
                                'gen_cost'  : None,
                                'ivtt'      : None,
                                'iwait'     : None,
                                'tdist'     : None,
                                'walk'      : None,
                                'xfer'      : None,
                                'xwait'     : None
                            },
                    'md' : {    'Fare'      : None,
                                'auto_cost' : None,
                                'ddist_dist': None,
                                'dtime'     : None,
                                'gen_cost'  : None,
                                'ivtt'      : None,
                                'iwait'     : None,
                                'tdist'     : None,
                                'walk'      : None,
                                'xfer'      : None,
                                'xwait'     : None
                            }
                }
        for period in periods:
            omxfn = skims_dir + r'\transit_skim_auto_' + period + '.omx'
            skim_omx = omx.open_file(omxfn,'r')
            for matrix in matrices:
                retval[period][matrix] = skim_omx[matrix]
            # end inner for
        # end outer for
        return retval
    # end_def
    
    def load_transit_walk_skims(self, skims_dir, periods=_skim_periods, matrices=_transit_walk_skim_matrices):
        """"
            Method: load_transit_walk_skims(self, skims_dir, periods=_skim_periods, matrices=_transit_walk_skim_matrices)
                    load TDM23 transit-auto skims as numPy arrays into a 2-level dictionary:
                    the first level of which is time period, the second level of which is matrix name
            
            Args:   skims_dir - root directory where TDM23 skim output can be found
                    period - list of time periods for which to read skims
                    matrices - list of skim matrices to read for each time period
            
            Returns: a 2-level dict containing the specified skim matrices as numPy arrays
            
            Raises: N/A
        """
        retval = {  'am' : {    'Fare'      : None,
                                'gen_cost'  : None,
                                'ivtt'      : None,
                                'iwait'     : None,
                                'walk'      : None,
                                'xfer'      : None,
                                'xwait'     : None
                            },
                    'md' : {    'Fare'      : None,
                                'gen_cost'  : None,
                                'ivtt'      : None,
                                'iwait'     : None,
                                'walk'      : None,
                                'xfer'      : None,
                                'xwait'     : None
                            }
                }
        for period in periods:
            omxfn = skims_dir + r'\transit_skim_walk_' + period + '.omx'
            skim_omx = omx.open_file(omxfn,'r')
            for matrix in matrices:
                retval[period][matrix] = skim_omx[matrix]
            # end inner for
        # end outer for
        return retval
    # end_def
# end_class SkimsMgr

###############################################################################
#
# Section 6: Dataframe and Geo-dataframe utilities
#
def export_df_to_csv(dataframe, csv_fn, column_list=None):
    """
    Function: export_df_to_csv

    Summary: Export columns in a dataframe to a CSV file.
             If a list of columns to export isn't specified, export all columns.

    Args: dataframe: Pandas dataframe
          csv_fn: Name of CSV file
          column_list: List of columns to export, or None

    Returns: N/A

    Raises: N/A
    """
    if column_list != None:
        dataframe.to_csv(csv_fn, column_list, sep=',')
    else:
        dataframe.to_csv(csv_fn, sep=',')
# end_def

def export_gdf_to_geojson(geo_dataframe, geojson_fn):
        geo_dataframe.to_file(geojson_fn, driver='GeoJSON')
# end_def

def export_gdf_to_shapefile(geo_dataframe, shapefile_fn):
        geo_dataframe.to_file(shapefile_fn, driver='ESRI Shapefile')
# end_def

def bbox_of_gdf(gdf):
    """
    Function: bbox_of_gdf

    Summary: Return the bounding box of all the features in a geo-dataframe.

    Args: gdf: a GeoPandas geo-dataframe

    Returns: Bounding box of all the features in the input geodataframe.
             The bounding box is returned as a dictionary with the keys: 
             { 'minx', 'miny', 'maxx', 'maxy'}.

    Raises: N/A
"""
    bounds_tuples = gdf['geometry'].map(lambda x: x.bounds)
    bounds_dicts = []
    for t in bounds_tuples:
        temp = { 'minx' : t[0], 'miny' : t[1], 'maxx' : t[2], 'maxy' : t[3] }
        bounds_dicts.append(temp)
    # end_for
    bounds_df = pd.DataFrame(bounds_dicts)
    minx = bounds_df['minx'].min()
    miny = bounds_df['miny'].min()
    maxx = bounds_df['maxx'].max()
    maxy = bounds_df['maxy'].max()
    retval = { 'minx' : minx, 'miny' : miny, 'maxx' : maxx, 'maxy' : maxy }
    return retval
# end_def bbox_of_gdf()

def center_of_bbox(bbox):
    """
    Function: center_of_bbox

    Summary: Given a geometric "bounding box", return its center point. 

    Args: bbox: Bounding box in the form of a dictionary with the keys { 'minx', 'miny', 'maxx', 'maxy' },
                e.g., one returned by bbox_of_gdf.

    Returns: Center point of the bounding box as a dictionary with the keys { 'x' , 'y' }.

    Raises: N/A
    """
    center_x = bbox['minx'] + (bbox['maxx'] - bbox['minx']) / 2
    center_y = bbox['miny'] + (bbox['maxy'] - bbox['miny']) / 2
    retval = { 'x' : center_x, 'y' : center_y }
    return retval
# end_def center_of_bbox()

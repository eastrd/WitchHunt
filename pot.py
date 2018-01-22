'''
This module is all about pot interface functions
'''

import db

db_name = "pot.sqlite"
tbl_name = "pot"

def Register(self, suffix_query, notif_method, template, counter_atk, will_expire_in):
    '''
    Add the given information into the Pot DB:
        - Generate url suffixes as Primary Keys from suffix_query
        - counter_atk is a list of all counter attack ids
        - will_expire_in is an integer minutes that this pot will be deleted in,
            needs to use _Calculate_timestamp to calculate the target timestamp.
    @Return: Number of url_suffixes FAILED to be added into the database
    '''
    num_of_registered_url_suffixes = 0
    url_suffix_list = _Suffix_query_parse(suffix_query)
    table = db.Connect_DB(db_name, tbl_name)
    for each_url_suffix in url_suffix_list:
        # Check if each url_suffix exists, if not, then add into the db
        if db.Exist(each_url_suffix):
            # Do nothing and goto the next url_suffix
            continue
        # Calculate valid_til timestamp
        valid_til = _Calculate_timestamp(int(will_expire_in))
        # Insert the new record into pot db
        table.insert({
            "url_suffix"    :   each_url_suffix,
            "suffix_query"  :   suffix_query,
            "notif_method"  :   notif_method,
            "template"      :   template,
            "counter_atk"   :   counter_atk,
            "valid_til"     :   valid_til
        })
        num_of_registered_url_suffixes += 1
    return len(url_suffix_list) - num_of_registered_url_suffixes

def Delete(self):
    '''
    Remove certain pots given the suffix_query
    '''
    pass

def _Calculate_timestamp(self, num_of_minutes):
    '''
    @Return: expire_timestamp = current_timestamp + num_of_minutes
    '''
    pass

def _Suffix_query_parse(self, suffix_syntax):
    '''
    Parses the suffix syntax query into a distinct list of url suffixes
    '''
    # Temporarily make url_suffix the same as the suffix query,
    #   need to change later on
    return [suffix_syntax]

def Get_all_pots(self):
    '''
    @Return all pots information in Json format
    '''
    pass

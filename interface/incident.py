'''
This module is all about incident interface functions
'''

from interface import db
import datetime
import json

db_name = "incident.sqlite"
tbl_name = "incident"

def Add(environ, pot_record):
    '''
    1. Add new record into incident database
    2. Notify the register
    3. Add / Update corresponding record in Attacker database
    @Return:
        True: if all actions are successful
        False: Otherwise
    '''
    try:
        # Construct and Add the new record into incident database
        data = {
            "atker_ip" : str(environ["HTTP_X_FORWARDED_FOR"]) if "HTTP_X_FORWARDED_FOR" in environ else environ["REMOTE_ADDR"],
            "atker_device" : str(environ["HTTP_USER_AGENT"]) if "HTTP_USER_AGENT" in environ else "",
            "url_suffix_visited" : pot_record["url_suffix"],
            "atk_triggered" : None,
            "timestamp" : int(datetime.datetime.now().timestamp())
        }
        db.Add(data, db_name, tbl_name)
        return True
    except Exception as e:
        print(e)
        return False

def _Delete(field, value):
    '''
    Deletes all incident_records matching the given field=value
    '''
    pass

def _Sendmail():
    '''
    Sends the email to the given destination with the given crafted messages
    '''
    pass

def Get_all_incident_records():
    '''
    Returns all incident records in json format
    '''
    pass

def Search_incident_record_by_atker_ip(atker_ip, is_json=False):
    '''
    Returns all incident records matching the given atker_ip,
        can specify whether the return value is json format or not. (Default: Dict)
    '''
    pass

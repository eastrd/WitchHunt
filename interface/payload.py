'''
This module is all about payload interface functions
'''

from interface import db, attacker
import datetime
import json

db_name = "payload.sqlite"
tbl_name = "payload"

def Add(name, desc, js_code):
    '''
    Add new payload information into database
    '''
    try:
        # Detect if payload with same name already exists
        if db.Exist("name", name, db_name, tbl_name):
            return False
        # Construct and Add the new record into payload database
        data = {
            "name" : name,
            "desc" : desc,
            "js_code" : js_code
        }
        db.Add(data, db_name, tbl_name)
        return True
    except Exception as e:
        print(e)
        return False

def Delete(name):
    '''
    Delete payload given the name
    '''
    return db.Remove("name", name, db_name, tbl_name)

def Save_result(environ, result_dict):
    '''
    Receive payload returns (optional)
    1. Store relevant information into attacker db
    2. Update triggered payload attacks in both attacker db and incident db
    '''
    if len(result_dict) > 0:
        ip = str(environ["HTTP_X_FORWARDED_FOR"]) if "HTTP_X_FORWARDED_FOR" in environ else environ["REMOTE_ADDR"]
        print("[!] Received Payload results from", ip)
        print(result_dict)
        # Merge all info in dict
        content = "\n".join(str(key) + " : " + result_dict[key] for key in result_dict.keys())
        attacker.Update_info(ip, content)
    return ""

def Get_all_payload_records():
    '''
    @Return: A JSON dict of all payload information.
    '''
    list_of_payloads = []
    list_of_payloads.append([each_payload for each_payload in db.Get_all_records(db_name, tbl_name)])
    return json.dumps(list_of_payloads).encode("utf-8")

def Search_payload_record_by_name(name, is_json=False):
    '''
    Return the payload information matching the given name,
        can specify whether the return value is json format or not. (Default: Dict)
    '''
    result = []
    for each_record in db.Search_all_records("name", name, db_name, tbl_name):
        result.append(each_record)
    if is_json:
        return json.dumps(result)
    return result

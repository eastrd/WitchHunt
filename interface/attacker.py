from interface import db
import requests
import simplejson as json
from simplejson import RawJSON

db_name = "attacker.sqlite"
tbl_name = "attacker"

def _maybe(dictionary, key):
    '''
    Similar to Maybe data type in Haskell.
    If key exists in given dictionary,
        return the string representation value corresponds to the key.
    Otherwise return empty string.
    '''
    if len(dictionary) > 0 and key in dictionary.keys():
        return str(dictionary[key])
    return ""

def Add(environ, pot_record):
    '''
    Takes the given requests.environ and pot record:
    1. Fetch the location API
    2. Fetch the ISP info
    3. Store all relevant information into attacker DB
    '''
    # Get IP from environment variable
    ip = str(environ["HTTP_X_FORWARDED_FOR"]) if "HTTP_X_FORWARDED_FOR" in environ else environ["REMOTE_ADDR"]
    if db.Exist("ip", ip, db_name, tbl_name):
        # If already exists record of this ip, terminate
        print("[!] Attacker IP already exists...")
        return
    # Get IP Information from external source

    else:
        response = ""
        try:
            # Make a request to fetch the detailed geo location regarding the prey
            response = requests.get("http://ip-api.com/json/" + ip).content
            # Convert json to dict
            response = json.loads(requests.get("http://ip-api.com/json/" + ip).content)
            if response["status"] == "fail":
                print("[!] Status shows fail for IP:", ip)
        except Exception as e:
            print("[!] Error occurred in fetching external IP info:", e)
        # Store the fetched information into attackerDB
        data = {
            "ip":   ip,
            "device": _maybe(environ, "HTTP_USER_AGENT"),
            "lat": _maybe(response, "lat"),
            "lon": _maybe(response, "lon"),
            "country": _maybe(response, "country"),
            "city": _maybe(response, "city"),
            "isp": _maybe(response, "isp"),
            "as": _maybe(response, "as"),
            "attacks_triggered": None,
            "other_info": None
        }
        db.Add(data, db_name, tbl_name)

def DeleteProfile(ip):
    '''
    Deletes records that matches the given ip
    '''
    pass

def Get_all_attackers_info():
    '''
    @Return: All attacker information in JSON format
    '''
    list_of_attackers = []
    list_of_attackers.append([each_attacker_record for each_attacker_record in db.Get_all_records(db_name, tbl_name)])
    return json.dumps(RawJSON(list_of_attackers)).encode("utf-8")

def Search_attacker_profile_by_ip(ip, is_json=False):
    '''
    @Return: (ONE?) attacker record that matches the given ip
    '''
    result = db.Search_one_record("ip", ip, db_name, tbl_name)
    if is_json:
        return json.dumps(RawJSON(result))
    return result

def Search_attacker_profile_by_device(ua):
    '''
    @Return: (ONE?) attacker record that matches the given User Agent
    '''
    result = db.Search_one_record("device", ua, db_name, tbl_name)
    if is_json:
        return json.dumps(RawJSON(result))
    return result

def Update_info(ip, content):
    print("[!] Writing %s for ip %s" %(content, ip))
    db.Update("ip", ip, "other_info", content, db_name, tbl_name)

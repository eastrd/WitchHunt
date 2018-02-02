from interface import db
import json

db_name = "attacker.sqlite"
tbl_name = "attacker"

def _maybe(dictionary, key):
    '''
    Similar to Maybe data type in Haskell.
    If key exists in given dictionary,
        return the string representation value corresponds to the key.
    Otherwise return empty string.
    '''
    if key in dictionary.keys():
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

    # Get IP Information from external source
    response = ""
    try:
        # Make a request to fetch the detailed geo location regarding the prey
        response = requests.get("http://ip-api.com/json/" + ip).content
        # Convert json to dict
        response = json.loads(requests.get("http://ip-api.com/json/" + ip).content)
    except Exception as e:
        print("[!] Error occurred in fetching external IP info:", e)

    if response["status"] == "fail":
        print("[!] Status shows fail for IP:", ip)
        
    else:
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
    pass

def Search_attacker_profile_by_ip(ip):
    '''
    @Return: (ONE?) attacker record that matches the given ip
    '''
    pass

def Search_attacker_profile_by_device(ua):
    '''
    @Return: (ONE?) attacker record that matches the given User Agent
    '''
    pass

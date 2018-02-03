from interface import pot, attacker, incident
from flask import request, Flask
import _thread as thread
import preset
import core

app = Flask(__name__)

@app.errorhandler(404)
def Handle(e=None):
    '''
    Receives all endpoint requests and Determine whether it's trapped or not
    '''
    url_suffix = "/".join(request.url.split("/")[3:])
    pot_record = pot.Search_pot_by_url_suffix(url_suffix)
    # As json.dumps(None) == null, but is_json option is not enabled, so pot_record is None
    if pot_record == None:
        # No pot is set at this endpoint
        # Default is 500 Internal Server Error
        return preset.HTML_500
    else:
        '''
        Honeypot is triggered in current url suffix:
            1. Store incident info into Incident DB
            2. Send an email notification as it adds into DB.
            3. Add atker info into attacker DB.
            4. Check with Counter attacker DB to check if any attack is triggered.
            5. If triggered, then update IncidentDB and AttackerDB.
        '''
        print("[!] Pot triggered!")
        # Fetch preset HTML for the attacker
        html_template = pot_record["template"]
        # Store incident information into IncidentDB
        if not incident.Add(request.environ, pot_record):
            print("[!!!] An error occurred when trying to add attacker information into incident DB")
        # Start a new thread to send the email
        thread.start_new_thread(core.Send_email, ("Email Thread", pot_record, request.environ))
        # Add attacker information into AtkerDB
        attacker.Add(environ, pot_record)
        # Return the pre-defined fake webpage
        return html_template



'''
RestAPIs
'''

# POT
@app.route("/api/pot/add", methods=["POST"])
def Add_pot():
    '''
    - Fetch user post data
    - Checks the pot's existance (ID => url_suffix) and Adds a new pot
    - All data are form-data
    '''
    project_name = request.form["project_name"]
    suffix_query = request.form["suffix_query"]
    template = request.form["template"]
    will_expire_in = int(request.form["expire"])
    notif_method = request.form["notif_method"]
    counter_atk = request.form["counter_atk"]

    if template == "500":
        html = preset.HTML_500
    elif template == "404":
        html = preset.HTML_400
    else:
        html = Scrape_page(content)

    num_need_to_register, num_registered = pot.Register(
        project_name,
        suffix_query,
        notif_method,
        html,
        counter_atk,
        will_expire_in
    )
    return (
        "%s out of %s honeypots failed to register"
        % (num_need_to_register-num_registered, num_need_to_register)
    )

@app.route("/api/pot/del", methods=["POST"])
def Del_pot():
    '''
    Removes certain pots based on url_suffix
    '''
    num_need_to_delete, num_deleted = pot.Delete(request.form["suffix_query"])
    return (
        "%s out of %s honeypots failed to delete"
        % (num_need_to_delete-num_deleted, num_need_to_delete)
    )

@app.route("/api/pot/all", methods=["GET"])
def See_all_pot():
    '''
    Display information of all pots
    '''
    return pot.Get_all_pots()


# Incident
@app.route("/api/incident/all", methods=["GET"])
def See_all_incidents():
    '''
    Display information of all incidents
    '''
    return incident.Get_all_incident_records()

@app.route("/api/incident/search", methods=["POST"])
def Search_incident_by_ip():
    '''
    Form data:
        ip : "ip"
    '''
    ip = request.form["ip"]
    return incident.Search_incident_records_by_atker_ip(ip, is_json=True)

@app.route("/api/incident/delete", methods=["POST"])
def Delete_incident_by_ip():
    '''
    Deletes all incident records matching the given atker_ip
    '''
    if incident.Delete("atker_ip", request.form["ip"]):
        return "Success"
    return "Failed"


# Attacker
@app.route("/api/attacker/all", methods=["GET"])
def See_all_attackers():
    '''
    Display information of all attackers
    '''
    return attacker.Get_all_attackers_info()

@app.route("/api/attacker/search_by_ip", methods=["POST"])
def Search_attacker_by_ip():
    '''
    Form data:
        ip : "ip"
    '''
    ip = request.form["ip"]
    return attacker.Search_attacker_profile_by_ip(ip, is_json=True)

@app.route("/api/attacker/search_by_ua", methods=["POST"])
def Search_attacker_by_ip():
    '''
    Form data:
        ua : "ua"
    '''
    ua = request.form["ua"]
    return attacker.Search_attacker_profile_by_ua(ua, is_json=True)

@app.after_request
def Fake_identity(response):
    '''
    Hides the original server header that shows Python framework, and replace
        it with a fake "nodejs".
    Later can be implemented to a given of random names to confuse the scanner
    '''
    response.headers["server"] = "nodejs"
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=12345)

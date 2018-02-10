from interface import pot, attacker, incident, payload
from flask import request, Flask, render_template
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
    '''
    Honeypot is triggered in current url suffix:
        1. Check if the url suffix is defined in Pot DB.
        2. If defined, craft HTML page with preset js_code.
        3. Store current incident info into Incident DB.
        4. Send email notification.
        5. Add basic attacker info into Attacker DB.

    When the payload return url is visited:
        1. Get the victim's POST data.
        2. Sanitize the victim input.
        3. Store the information in Attacker DB under "Other Info".
        4. Update Attacker DB and corresponding Incident DB's payload_triggered columns.
        5. Notify the user regarding the new information.
    '''
    print("[!] Pot triggered!")
    # Fetch preset HTML for the attacker
    page = pot.Craft_payload(pot_record)
    # Store incident information into IncidentDB
    if not incident.Add(request.environ, pot_record):
        print("[!!!] An error occurred when trying to add attacker information into incident DB")
    # Start a new thread to send the email
    email = pot_record["notif_method"]
    if len(email) > 0 and "@" in email:
        project_name = pot_record["project_name"]
        thread.start_new_thread(core.Send_email, ("Email Thread", email, project_name, request.environ))
    # Add attacker information into AtkerDB
    attacker.Add(request.environ, pot_record)
    # Return the pre-defined fake webpage
    return page


'''
                            Frontend
'''
@app.route("/pot")
def Pot_page():
    '''
    1. Loads all pots onto a list
    2. User can add/del/search a pot
    '''
    return render_template("pot.html")

@app.route("/payload")
def Payload_page():
    '''
    1. Loads all payloads onto a list
    2. User can add/search/del a payload
    '''
    return render_template("payload.html")

@app.route("/incident")
def Incident_page():
    '''
    1. Loads all incidents onto a list
    2. User can search/del an incident
    '''
    return render_template("incident.html")

@app.route("/attacker")
def Attacker_page():
    '''
    1. Loads all attacker records onto a list
    2. User can search attackers by ip or ua
    '''
    return render_template("attacker.html")


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
    js_code_name = request.form["js_code_name"]

    if template == "":
        html = "<html><head></head><body></body></html>"
    elif template == "500":
        html = preset.HTML_500
    elif template == "404":
        html = preset.HTML_400
    else:
        html = core.Scrape_page(content)

    num_need_to_register, num_registered = pot.Register(
        project_name,
        suffix_query,
        notif_method,
        html,
        js_code_name,
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
    return core.Escape_special_chars(str(pot.Get_all_pots()))



# Incident
@app.route("/api/incident/all", methods=["GET"])
def See_all_incidents():
    '''
    Display information of all incidents
    '''
    return core.Escape_special_chars(str(incident.Get_all_incident_records()))

@app.route("/api/incident/search", methods=["POST"])
def Search_incident_by_ip():
    '''
    Form data:
        ip : "ip"
    '''
    ip = request.form["ip"]
    return core.Escape_special_chars(str(incident.Search_incident_records_by_atker_ip(ip, is_json=True)))

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
    return core.Escape_special_chars(str(attacker.Get_all_attackers_info()))

@app.route("/api/attacker/search_by_ip", methods=["POST"])
def Search_attacker_by_ip():
    '''
    Form data:
        ip : "ip"
    '''
    ip = request.form["ip"]
    return core.Escape_special_chars(str(attacker.Search_attacker_profile_by_ip(ip, is_json=True)))

@app.route("/api/attacker/search_by_ua", methods=["POST"])
def Search_attacker_by_ua():
    '''
    Form data:
        ua : "ua"
    '''
    ua = request.form["ua"]
    return core.Escape_special_chars(str(attacker.Search_attacker_profile_by_ua(ua, is_json=True)))



# Payload
@app.route("/api/payload/add", methods=["POST"])
def Add_payload():
    name = request.form["name"]
    description = request.form["desc"]
    js_code = request.form["js_code"]
    # print("[~] Going to add payload:\n%s:%s\n%s" %(name, description, js_code))
    return "Payload Added" if payload.Add(name, description, js_code) else "Payload failed to add"

@app.route("/api/payload/search_by_name", methods=["POST"])
def Search_payload_by_name():
    '''
    Form data:
        name : "name"
    '''
    name = request.form["name"]
    return core.Escape_special_chars(str(payload.Search_payload_by_name(name, is_json=True)))

@app.route("/api/payload/all", methods=["GET"])
def See_all_payloads():
    return core.Escape_special_chars(str(payload.Get_all_payload_records()))

@app.route("/api/payload/del", methods=["POST"])
def Del_payload_by_name():
    name = request.form["name"]
    return "Deleted" if payload.Delete(name) else "Failed to delete"

@app.route("/ap", methods=["GET", "POST"])
def Receive_payload_results():
    return core.Escape_special_chars(str(payload.Save_result(request.environ, request.args)))



# Others
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

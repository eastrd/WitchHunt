from flask import request, Flask
import _thread as thread
import dataset
import preset
import core

app = Flask(__name__)

@app.errorhandler(404)
def Handle(e=None):
    '''
    Receives all endpoint requests and Determine whether it's trapped or not
    '''
    suffix = "/".join(request.url.split("/")[3:])

    # Connect to SQLite db
    pot_table = core.Connect_DB("pots.sqlite", "Case")

    result = pot_table.find_one(url=suffix)

    if result is None:
        # No pot is set at this endpoint
        return preset.HTML_500
    else:
        # The targeted idiot hits our pot
        print("[!] Pot triggered!")
        email_title = "WitchHunt Notification: " + result["notes"]
        email_addr = result["email"]
        html = result["content"]
        valid_time = result["expiry"]

        # Get all information about the prey
        report = core.Get_attaker_info(request.environ)
        thread.start_new_thread(core.Send_email, ("Email Thread", email_addr, email_title, report))
        # Return the pre-defined fake webpage
        return html

@app.route("/api/pots/add", methods=["POST"])
def Add_pot():
    '''
    - Fetch user post data
    - Checks the pot's existance (ID => url_suffix) and Adds a new pot
    - All data are form-data
    '''
    notes = request.form["notes"]
    url_suffix = request.form["url"]
    content = request.form["content"]
    duration = int(request.form["time"])
    email = request.form["email"]
    if_setup_successful = core.Deploy_pot(notes, url_suffix, content, duration, email)
    return "Pot added successfully" if if_setup_successful else "Pot already exists"

@app.route("/api/pots/del", methods=["POST"])
def Del_pot():
    '''
    Removes certain pots based on url_suffix
    '''
    pots_

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

from core import SendEmail, ScrapePage, SetTrap, GetPreyInfo
from flask import request, render_template, Flask
from ast import literal_eval
import _thread as thread
import requests
import smtplib
import dataset

app = Flask(__name__)

@app.errorhandler(404)
def OFortuna(e=None):
    '''
    Handles all trap and non-trap requests
    '''
    suffix = "/".join(request.url.split("/")[3:])

    # Connect to SQLite in-memory db
    trapDb = dataset.connect("sqlite:///:memory:")
    trapTbl = trapDb["Case"]

    result = trapTbl.find_one(url=suffix)
    if result is None:
        # No trap is set at this endpoint
        return render_template("500.html")
    else:
        # [!] Trap is triggered
        # Fetch all releavent information from database records
        trap_url = request.url
        email_title = "[!] " + result["notes"]
        email_addr = result["email"]
        html = result["content"]
        valid_time = result["time"]
        # Get all information about the prey
        report = GetPreyInfo(request.environ)
        thread.start_new_thread(SendEmail,
                                ("Email Thread", email_addr, email_title, report))
        # Return the pre-defined fake webpage
        return html


@app.route("/tavern", methods=["GET", "POST"])
def PlaceDemand():
    '''
    Returns the configuration page for user to create new trap endpoint
    '''
    if request.method == "POST":
        # Fetch Settings
        notes = request.form["notes"]
        url = request.form["url"]
        content = request.form["content"]
        time = request.form["time"]
        email = request.form["email"]

        ifAlreadySetup = SetTrap(notes, url, content, time, email)
        return "1" if ifAlreadySetup else "0"
    else:
        return render_template("demand.html")


@app.after_request
def apply_caching(response):
    '''
    Hides the original server header that shows Python framework, and replace
        it with a fake "nodejs"
    '''
    response.headers["Server"] = "nodejs"
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=12345)

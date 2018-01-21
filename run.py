from flask import request, render_template, Flask
import _thread as thread
import dataset
import preset
import core

app = Flask(__name__)

@app.errorhandler(404)
def OFortuna(e=None):
    '''
    Handles all pot & non-pot requests
    '''
    suffix = "/".join(request.url.split("/")[3:])

    # Connect to SQLite db
    potTbl = core.ConnectDB("pots.sqlite", "Case")

    result = potTbl.find_one(url=suffix)

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
        report = core.GetPreyInfo(request.environ)
        thread.start_new_thread(core.SendEmail, ("Email Thread", email_addr, email_title, report))
        # Return the pre-defined fake webpage
        return html

@app.route("/ip")
def IndexPage():
    return request.environ

@app.route("/tavern", methods=["GET", "POST"])
def PlaceDemand():
    '''
    Clears the expired pots
        AND
    Returns the configuration page for user to create new pot endpoint
    '''
    if request.method == "POST":
        # Fetch settings from user
        notes = request.form["notes"]
        url = request.form["url"]
        content = request.form["content"]
        duration = int(request.form["time"])
        email = request.form["email"]
        ifAlreadySetup = core.DeployPot(notes, url, content, duration, email)
        return "1" if ifAlreadySetup else "0"
    else:
        # It's a GET method, displays the setting page to user
        core.WashDb()
        return render_template("demand.html")


@app.after_request
def apply_caching(response):
    '''
    Hides the original server header that shows Python framework, and replace
        it with a fake "nodejs".
    Later can be implemented to a given of random names to confuse the scanner
    '''
    response.headers["Server"] = "nodejs"
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=12345)

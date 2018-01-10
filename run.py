from flask import request, render_template, Flask
from core import SendEmail, ScrapePage
from ast import literal_eval
import _thread as thread
import requests
import smtplib
import dataset

app = Flask(__name__)


def GetPreyInfo():
    # Generates a report regarding the prey who triggers the trap
    environ = request.environ
    ip = str(environ["REMOTE_ADDR"]) if "REMOTE_ADDR" in environ else ""
    port = str(environ["REMOTE_PORT"]) if "REMOTE_PORT" in environ else ""
    ua = str(environ["HTTP_USER_AGENT"]
             ) if "HTTP_USER_AGENT" in environ else ""
    method = str(environ["REQUEST_METHOD"]
                 ) if "REQUEST_METHOD" in environ else ""
    path = str(environ["PATH_INFO"]) if "PATH_INFO" in environ else ""
    query = str(environ["QUERY_STRING"]) if "QUERY_STRING" in environ else ""
    cookie = str(environ["HTTP_COOKIE"]) if "HTTP_COOKIE" in environ else ""
    language = str(environ["HTTP_ACCEPT_LANGUAGE"]
                   ) if "HTTP_ACCEPT_LANGUAGE" in environ else ""
    encoding = str(environ["HTTP_ACCEPT_ENCODING"]
                   ) if "HTTP_ACCEPT_ENCODING" in environ else ""
    accept = str(environ["HTTP_ACCEPT"]) if "HTTP_ACCEPT" in environ else ""
    # Make a request to fetch the detailed geo location regarding the prey
    response = requests.get("http://ip-api.com/json/" + ip).content
    # Convert String presentation of dict into a proper dict
    response = literal_eval(str(response)[2:-1])
    # Construct the report
    report = "Prey Information:\n\t" +\
        "IP: " + ip + "\n\t" +\
        "PORT: " + port + "\n\t" +\
        "User Agent: " + ua + "\n\t" +\
        "Request Method: " + method + "\n\t" +\
        "Path:" + path + "\n\t" +\
        "Query: " + query + "\n\t" +\
        "Cookie: " + cookie + "\n\t" +\
        "Language: " + language + "\n\t" +\
        "Encoding: " + encoding + "\n\t" +\
        "Accept: " + accept + "\n\n" + \
        "Geolocation Analysis:\n"
    for key in response.keys():
        report += "\t" + str(key) + ": " + str(response[key]) + "\n"
    return report


def SetTrap(notes, url, content, time, email):
    '''
    Set up the honeypot webpage given the information
    @Return: True if setup successful, False otherwise
    '''

    # Connect to SQLite in-memory db
    trapDb = dataset.connect("sqlite:///:memory:")
    trapTbl = trapDb["Case"]

    # Check if endpoint already exists in trap table
    result = trapTbl.find_one(url=url)
    if result is not None:
        return False
    else:
        # Change content variable into the html source it's pointing to
        if content == "500":
            html = render_template("500.html")
        elif content == "404":
            html = render_template("404.html")
        else:
            html = ScrapePage(content)

        trapTbl.insert({
            "notes": notes,
            "url": url,
            "content": html,
            "time": time,
            "email": email
        })
    return True


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
        report = GetPreyInfo()
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


app.run(host="0.0.0.0", debug=False, port=80)


# Need to get currrent timestamp of the time when set up
# If record already exist during setup, check if the existing record has expired, if so, overwrite.
# Calculate the expiry time when put in trapDb

from flask import request, Flask
import _thread as thread
import preset
import core
import pot

app = Flask(__name__)

@app.errorhandler(404)
def Handle(e=None):
    '''
    Receives all endpoint requests and Determine whether it's trapped or not
    '''
    url_suffix = "/".join(request.url.split("/")[3:])

    record = pot.Get_record(url_suffix)

    if record is None:
        # No pot is set at this endpoint
        # Default is 500 Internal Server Error
        return preset.HTML_500
    else:
        # The target has hit our pot
        print("[!] Pot triggered!")
        email_title = "[WitchHunt Notification] " + record["project_name"]
        email_addr = record["notif_method"]
        html = record["template"]
        valid_time = record["valid_til"]

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

@app.route("/api/pots/del", methods=["POST"])
def Del_pot():
    '''
    Removes certain pots based on url_suffix
    '''
    num_need_to_delete, num_deleted = pot.Delete(request.form["suffix_query"])
    return (
        "%s out of %s honeypots failed to delete"
        % (num_need_to_delete-num_deleted, num_need_to_delete)
    )


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

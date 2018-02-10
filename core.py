from datetime import datetime
from ast import literal_eval
import requests
import smtplib
import dataset
import preset


def Wash_DB():
    '''
    Monitors and cleans the expired pots in the database
    '''
    current_timestamp = int(datetime.now().timestamp())

    # Connect to SQLite db
    pot_table = Connect_DB("pots.sqlite", "Case")
    if len(pot_table) == 0:
        # Check if the table is empty, if so then no need to continue further
        return
    for record in pot_table:
        # Delete expired records
        if record["expiry"] <= current_timestamp:
            print("[!] Project Expired:", record["notes"])
            pot_table.delete(id=record["id"])

def Send_email(threadName, email_address, project_name, environ):
    try:
        # Construct email meta-data
        email_title = "[WitchHunt Notification] " + project_name

        body = Get_attaker_info(environ)

        # Send the email report
        gmail_user = 'wpetrap@gmail.com'
        gmail_password = 'camiziwetazi'
        to = [email_address]
        email_text = "From: %s\nTo: %s\nSubject: %s\n\n%s" \
            % (gmail_user, ", ".join(to), email_title, body)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to, email_text.encode("utf-8").strip())
        server.close()
        print('Email sent!')
    except Exception as e:
        print('[!] Error occurred in Sending Email:', e)

def Scrape_page(target_url):
    # Creates a selenium instance to fetch the webpage source
    # Returns the webpage html given url
    # If phantomJS fails then try basic requests
    from selenium import webdriver
    import os
    if "http" not in target_url:
        target_url = "http://" + target_url
    try:
        driver = webdriver.PhantomJS()
        driver.get(target_url)
        source = driver.page_source
        driver.quit()
        # Remove log file
        os.remove("ghostdriver.log")
    except:
        source = requests.get(target_url).content
    return source

def Get_attaker_info(environ):
    '''
    Generates a report regarding the prey who triggers the trap
    @ environ: Flask's built-in environment variable list
    @ Return: A full string report ready to be sent to destination email
    '''
    # As the ip will always be proxyed by Nginx
    #   so HTTP_X_FORWARDED_FOR will always be there for the real ip
    ip = str(environ["HTTP_X_FORWARDED_FOR"]) if "HTTP_X_FORWARDED_FOR" in environ else environ["REMOTE_ADDR"]
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

    # Get IP Information from external source
    response = ""
    try:
        # Make a request to fetch the detailed geo location regarding the prey
        response = requests.get("http://ip-api.com/json/" + ip).content

        # Convert String presentation of dict into a proper dict
        response = literal_eval(str(response)[2:-1])

        # Construct the report
        for key in response.keys():
            report += "\t" + str(key) + ": " + str(response[key]) + "\n"
    except Exception as e:
        print("[!] Error occurred in requesting IP info:", e)

    return report



def Escape_special_chars(dirty_string):
    return dirty_string.replace("<", "&lt;").replace(">", "&gt;")

import dataset

def SendEmail(threadName, emailAddr, subject, body):
    # Construct and sends the email report
    gmail_user = 'wpetrap@gmail.com'
    gmail_password = 'camiziwetazi'
    to = [emailAddr]
    email_text = "From: %s\nTo: %s\nSubject: %s\n\n%s" \
        % (gmail_user, ", ".join(to), subject, body)
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(gmail_user, to, email_text.encode("utf-8").strip())
    server.close()
    print('Email sent!')


def ScrapePage(target_url):
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
            html = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"><title>500 Internal Server Error</title><h1>Internal Server Error</h1><p>The server encountered an internal error and was unable to complete your request.  Either the server is overloaded or there is an error in the application.</p>'''
        elif content == "404":
            html = '''<html><head><title>404 Not Found</title></head><body><h1>Not Found</h1>The requested URL was not found on this server.</body></html>'''
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


def GetPreyInfo(environ):
    '''
    Generates a report regarding the prey who triggers the trap
    @ environ: Flask's built-in environment variable list
    @ Return: A full string report ready to be sent to destination email
    '''
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

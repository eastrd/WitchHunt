from datetime import datetime
from ast import literal_eval
import configparser
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

def Escape_special_chars(dirty_string):
    return dirty_string.replace("<", "&lt;").replace(">", "&gt;")

def Get_whitelist_ip(config_filename):
    '''
    @Return: List of white listed IP addresses
    '''
    cf = configparser.ConfigParser()
    cf.read(config_filename)
    ip_list = str(cf.get("Whitelist IP", "IP")).split(",")
    return ip_list

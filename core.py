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

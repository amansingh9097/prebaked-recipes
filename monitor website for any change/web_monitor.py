import requests
from bs4 import BeautifulSoup
import time
import smtplib

while True:
    # set the url as the website to monitor,
    url = "https://www.gatesnotes.com/About-Bill-Gates/Summer-Books-2020"
    # set the headers like we are on a browser,
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # download the homepage
    response = requests.get(url, headers=headers)
    # parse the downloaded homepage and grab all text,
    soup = BeautifulSoup(response.text, "lxml")
    
    # if the number of times the word "Kaggle" occurs on the page is less than 1,
    if str(soup).find("books") == -1:
        # wait 60 seconds,
        time.sleep(60)
        # continue with the script,
        continue
        
    # but if the word "books" occurs any other number of times,
    else:
        # create an email message with just a subject line,
        msg = 'Subject: This is Aman\'s script talking, you should CHECK {}!'.format(url)
        # set the 'from' address,
        fromaddr = 'amansingh9097@gmail.com'
        yourpass = 'xxxxx'
        # set the 'to' addresses,
        toaddrs  = ['eenameenadeeka@gmail.com','yabadabadoo@yahoo.com']
        
        # setup the email server,
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # add my account login name and password,
        server.login(fromaddr, yourpass)
        
        ## Print the email's contents
        # print('From: ' + fromaddr)
        # print('To: ' + str(toaddrs))
        # print('Message: ' + msg)
        
        # send the email
        server.sendmail(fromaddr, toaddrs, msg)
        disconnect from the server
        server.quit()
        
        break
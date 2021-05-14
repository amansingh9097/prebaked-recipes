import time
import hashlib
from urllib.request import urlopen, Request

# set the url as the website to monitor,
url = "https://www.gatesnotes.com/About-Bill-Gates/Summer-Books-2020"
# set the headers like we are on a browser,
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
# download the homepage
response = requests.get(url, headers=headers)

# create the initial hash
currentHash = hashlib.sha224(response).hexdigest()
print("running")
time.sleep(10)

while True:
    try:
        # perform the get request
        response = urlopen(url).read()
          
        # create a hash
        currentHash = hashlib.sha224(response).hexdigest()
          
        # time delay
        time.sleep(30)
          
        # perform the get request
        response = urlopen(url).read()
          
        # create a new hash
        newHash = hashlib.sha224(response).hexdigest()
  
        # if new hash is same as the previous hash
        if newHash == currentHash:
            continue
  
        # if something changed in the hashes
        else:
            # notify
            print("something changed")
  
            # again read the website
            response = urlopen(url).read()
  
            # create a hash
            currentHash = hashlib.sha224(response).hexdigest()
  
            # wait for 30 seconds
            time.sleep(30)
            
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
      
            continue
              
    # To handle exceptions
    except Exception as e:
        print("error")

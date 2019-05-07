# utf-8
# author: Aman Singh (amansingh9097@gmail.com)
# Creation Date: 07-May-2019

import smtplib
from config import Config as cfg
from datetime import datetime
from read_from_files import get_contacts, read_template

# send the msg via our own SMTP server.
s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
s.starttls()
PASSWORD = cfg['login']['my_pass']  # input("Enter your password")
s.login(cfg['login']['my_user'], PASSWORD)

names, emails = get_contacts(cfg['contacts']['C_FILE'])  # read contacts from file
message_template = read_template(cfg['message']['M_FILE'])  # read msg from file

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# for each contact, send the email
for name, email in zip(names, emails):
    msg = MIMEMultipart()  # create a message

    # add in the actual person name to the message template
    message = message_template.substitute(PERSON_NAME=name.title())

    # setup the parameters of the message
    msg['From'] = cfg['mail']['FROM']
    msg['To'] = email
    msg['Subject'] = cfg['mail']['SUBJECT'] + ": " + datetime.today().strftime('%d-%m-%Y')

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # send the msg via the server set up earlier
    s.send_message(msg)

    # delete the MIMEMultipart object and re-create it at each iteration of the loop
    del msg

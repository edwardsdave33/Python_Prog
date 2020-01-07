import requests
import smtplib
import datetime
import smtplib
import cryptography
import os
from bs4 import BeautifulSoup


import requests
import smtplib
import datetime
import smtplib
import cryptography
import os
from bs4 import BeautifulSoup


result = requests.get("http://download.videolan.org/pub/videolan/vlc/")
src= result.content
soup = BeautifulSoup(src, 'lxml')

today = datetime.date.today().strftime("%d-%b-%Y")
text= str(soup.text)

if today in text:

    from cryptography.fernet import Fernet

    key = b'UjuWAWXM0wCYJBs1nTaOQYID0WjMsa7nahFdp4eubMw='
    output_file = 'path/app_pwd.encrypted'
    output_file2 = 'path/app_pwd.decrypted'

    with open(output_file, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.decrypt(data)

    with open(output_file2, 'wb') as f:
        f.write(encrypted)

    f = open(output_file2, "r")
    if f.mode == 'r':
        contents = f.read()
        gmail_password = contents
    os.remove(output_file2)
    gmail_user = 'email'
    to = ['email']
    sent_from = gmail_user
    subject = 'VLC Security Update'
    body = today + " " + "VLC Update"

    email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong...')

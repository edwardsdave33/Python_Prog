import requests
import smtplib
import datetime
import smtplib
import cryptography
import os
from bs4 import BeautifulSoup


result = requests.get("https://www.7-zip.org/download.html")
src= result.content

soup = BeautifulSoup(src, 'lxml')
links = soup.find_all("b")
today = datetime.date.today().strftime("%Y-%m-%d")


for link in links:
    if today in link.text:
       
       # encrypt

       from cryptography.fernet import Fernet

       key = b'UjuWAWXM0wCYJBs1nTaOQYID0WjMsa7nahFdp4eubMw='
       output_file = '/users/david/k2e/app_pwd.encrypted'
       output_file2 = '/users/david/k2e/app_pwd.decrypted'

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
       gmail_user = 'david.edwards@k2esec.com'
       to = ['david.alex.edwards@gmail.com']
       sent_from = gmail_user
       subject = '7ZIP Security Update'
       body = "Update" + "" + link.text.replace('Download', '')

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





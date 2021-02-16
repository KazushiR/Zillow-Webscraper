import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from Zillow_API import prices, json_object
import pandas as pd
import json, smtplib, ssl

def Email(body,recipients,key, html_object):
    smtpobj = smtplib.SMTP("smtp.gmail.com", 587)
    msg = MIMEMultipart()
    msg.attach(MIMEText(body,'text'))
    part = MIMEBase('text', "html")
    part.set_payload(html_object)
    part.add_header('Content-Disposition', 'attachment; filename="tbl.html"')
    msg.attach(part)
    sender = 'kazushipythontest@gmail.com'
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = "Html Test"
    print(f"Mail Sent to {sender}")
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.login("username", "Password")
    smtpobj.sendmail(sender, recipients, msg.as_string())
    smtpobj.close()


information = json.loads(json_object)
df = pd.DataFrame([(key, L[0], L[1]) for (key, L) in information.items()], columns = ["Websites", "Bedrooms", "Address"])
pd.set_option('display.max_columns', None)
df["Prices"] = prices
Email("Please see Attached for HTML File.", ["Recepient"], key="", html_object=df.to_html())

#!/usr/bin/env python

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import time


def notify(
        text, subject, to_email, from_email,
        password, host="smtp.gmail.com", port=587, **kwargs):
    if not isinstance(to_email, (list, tuple)):
        to_email = [to_email, ]
    body = "%s\n" % text
    body = "Time of exception: %s" % time.ctime()
    for kw in kwargs:
        body += "\t%s = %s\n" % (kw, kwargs[kw])
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = ','.join(to_email)
    text = MIMEText(body, 'plain')
    msg.attach(text)
    s = smtplib.SMTP()
    s.connect(host, port)
    s.starttls()
    s.login(from_email, password)
    s.sendmail(from_email, to_email, msg.as_string())
    s.quit()


#!/usr/bin/env python

import ConfigParser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
import time


default_host = 'smtp.gmail.com'
default_port = 587


def load_config(filename="~/.notifier.ini"):
    filename = os.path.expanduser(filename)
    if not os.path.exists(filename):
        return {}
    cp = ConfigParser.SafeConfigParser()
    cp.read(filename)
    return dict(cp.items('notifier'))


def notify(
        text, subject, to_email, from_email=None,
        password=None, host=None, port=None, **kwargs):
    cfg = load_config()
    if from_email is None:
        from_email = cfg['from_email']
    if password is None:
        password = cfg['password']
    if host is None:
        host = cfg.get('host', default_host)
    if port is None:
        port = cfg.get('port', default_port)
    if not isinstance(to_email, (list, tuple)):
        to_email = [to_email, ]
    body = "%s\n" % text
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

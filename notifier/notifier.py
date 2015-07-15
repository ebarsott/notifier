#!/usr/bin/env python

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import time

from . import config


def send_notification(text, subject=None, to_email=None, cfg=None):
    dcfg = config.load_config()
    if isinstance(cfg, dict):
        dcfg.update(cfg)
    cfg = config.resolve_config(dcfg)
    config.validate_config(cfg)
    if to_email is None:
        if 'to_email' not in cfg:
            raise KeyError("Notifier missing to_email")
        to_email = cfg['to_email']
    if not isinstance(to_email, (list, tuple)):
        to_email = [to_email, ]
    if subject is None:
        subject = "Notification: %s" % time.time()
    body = "%s\n" % text
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = cfg['from_email']
    msg['To'] = ','.join(to_email)
    text = MIMEText(body, 'plain')
    msg.attach(text)
    s = smtplib.SMTP()
    s.connect(cfg['host'], cfg['port'])
    s.starttls()
    s.login(cfg['from_email'], cfg['password'])
    s.sendmail(cfg['from_email'], to_email, msg.as_string())
    s.quit()


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

#!/usr/bin/env python

import configparser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
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


default_host = 'smtp.gmail.com'
default_port = 587


def load_config(filename="~/.notifier.ini"):
    filename = os.path.expanduser(filename)
    if not os.path.exists(filename):
        return {}
    cp = configparser.SafeConfigParser()
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

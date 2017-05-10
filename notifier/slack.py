#!/usr/bin/env python

import os

import slackclient


def channel_message(text, channel):
    """Requires a slack token stored in the SLACK_TOKEN environment variable"""
    c = slackclient.SlackClient(os.environ['SLACK_TOKEN'])
    c.api_call(
        'chat.postMessage',
        channel=channel,
        text=text)

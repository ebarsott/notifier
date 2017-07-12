#!/usr/bin/env python

import os

import slackclient


def channel_message(text, channel, token=None):
    """Requires a slack token stored in the SLACK_TOKEN environment variable"""
    if token is None:
        token = os.environ['SLACK_TOKEN']
    c = slackclient.SlackClient(token)
    c.api_call(
        'chat.postMessage',
        channel=channel,
        text=text)

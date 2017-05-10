#!/usr/bin/env python

from . import notifier
from .notifier import notify, send_notification


__all__ = ['notifier', 'notify', 'send_notification']

try:
    import slackclient
    from .slack import channel_message
    __all__.append('channel_message')
except ImportError:
    pass

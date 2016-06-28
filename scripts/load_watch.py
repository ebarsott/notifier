#!/usr/bin/env python
"""
Watch the system load.

When it falls below a certain threshold, send a notification.
"""

import argparse
import os
import time

import notifier


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-l', '--load', default=1.0, type=float,
        help="load threshold for notification")
    parser.add_argument(
        '-t', '--polltime', default=1.0, type=float,
        help="time between load checks")
    parser.add_argument(
        '-m', '--message', default="", type=str,
        help="message to include in notification")
    parser.add_argument(
        '-s', '--subject', default="Load threshold hit", type=str,
        help="subject to include in notification")
    parser.add_argument(
        '-e', '--email', default="", type=str,
        help="send notification to this email")
    parser.add_argument(
        '-v', '--verbose', default=False, action='store_true',
        help="enable verbose output")
    args = parser.parse_args()
    if args.verbose:
        print("Arguments: %s" % args)

    if args.email == "":
        raise Exception("Missing email: %s" % args.email)
    l = os.getloadavg()[0]
    while l > args.load:
        if args.verbose:
            print("Current load: %s" % l)
        time.sleep(args.polltime)
        l = os.getloadavg()[0]

    msg = 'Load fell below threshold %s' % args.load
    if args.message != '':
        msg += '\n' + args.message
    if args.verbose:
        print(
            "Sending notification[to %s]: %s, %s" %
            (args.email, args.subject, msg))
    notifier.notify(msg, args.subject, args.email)


if __name__ == '__main__':
    main()

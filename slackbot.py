#!/usr/bin/env python3

import socket
from os import environ
from datetime import datetime, timedelta
from time import sleep

from slackclient import SlackClient

from oxycsbot import OxyCSBot


def bind_socket():
    sock = socket.socket()
    sock.bind(('', int(environ['PORT'])))
    sock.listen(1)
    conn, addr = sock.accept()


def run():
    print('Running!')
    start = datetime.now()
    token = environ['TOKEN']
    slack_client = SlackClient(token)
    if not slack_client.rtm_connect(with_team_state=False):
        print("Connection failed. Exception traceback printed above.")
        return
    bot_id = slack_client.api_call('auth.test')['user_id']
    print(bot_id)
    # check for direct mention events
    bot = OxyCSBot() # FIXME
    while True:
        for event in slack_client.rtm_read():
            print(event)
            if event['type'] != 'message' or 'subtype' in event:
                continue
            if ' ' not in event['text']:
                continue
            user_id, message = event['text'].split(' ', maxsplit=1)
            if user_id == f'<@{bot_id}>':
                message = message.strip()
                channel = event['channel']
                if message:
                    response = bot.respond(message)
                    slack_client.api_call('chat.postMessage', channel=channel, text=response)
        sleep(1)


def main():
    bind_socket()
    run()


if __name__ == '__main__':
    main()

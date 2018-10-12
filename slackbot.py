#!/usr/bin/env python3

from os import environ
from time import sleep

from slackclient import SlackClient

from oxycsbot import OxyCSBot


def run():
    print('bot running')
    token = environ['TOKEN']
    print(f'found Slack token {token}')
    slack_client = SlackClient(token)
    if not slack_client.rtm_connect(with_team_state=False):
        print("connection failed; exception traceback is above.")
        return
    bot_id = slack_client.api_call('auth.test')['user_id']
    print(f'assigned bot ID {bot_id}')
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


if __name__ == '__main__':
    run()

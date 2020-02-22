#!/usr/bin/env python3
"""An interface to Slack for chatbots."""

import ssl
from os import environ
from time import sleep

import certifi
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter

from oxycsbot import OxyCSBot # FIXME replace with your chatbot class

# initialize the Flask app
app = Flask(__name__)

# initialize the Slack objects
slack_events_adapter = SlackEventAdapter(environ['SLACK_SIGNING_SECRET'], '/slack/events', app)
slack_web_client = WebClient(token=environ['SLACK_BOT_TOKEN'])

global_state = {
    'bot_id': slack_web_client.auth_test()['user_id'],
    'partners': {},
}


@slack_events_adapter.on('message')
def message(payload):
    """Pass messages onto a per user, per channel chatbot instance."""
    event = payload.get('event', {})

    bot_id = global_state['bot_id']
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    if user_id == bot_id:
        return
    if not text:
        return

    key = (user_id, channel_id)
    if key not in global_state['partners']:
        global_state['partners'][key] = OxyCSBot() # FIXME replace with your chatbot class
    chatbot = global_state['partners'][key]
    response = chatbot.respond(text)

    slack_web_client.chat_postMessage(
        channel=channel_id,
        text=response,
    )


def main():
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    app.run()


if __name__ == '__main__':
    main()

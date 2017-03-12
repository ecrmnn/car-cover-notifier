#!/usr/bin/env python
# -*- coding: utf-8 -*-

from slackclient import SlackClient

class Slack:
    def __init__(self, token, channel):
        self.token = token
        self.channel = channel

    def send_message(self, temperature):
        slack = SlackClient(self.token)
        slack.api_call(
            "chat.postMessage",
            channel=self.channel,
            text='I morgen er blir det ' + temperature + ' grader. Sett på biltrekket!',
            as_user=True,
            link_names=True
        )
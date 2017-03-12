#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests
import xmltodict
import datetime
from slack import Slack
from os import environ as env
from os.path import join, dirname
from dotenv import load_dotenv

# Load enviroment variables from .env
load_dotenv(join(dirname(__file__), '.env'))

url = 'http://www.yr.no/place/' + env.get('YR_PLACE') + '/forecast_hour_by_hour.xml'
response = requests.get(url).text

parsedXmlResponse = xmltodict.parse(response)
times = parsedXmlResponse['weatherdata']['forecast']['tabular']['time']

def convertToTimestamp(hour):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    return str(tomorrow) + hour

hours = ['T04:00:00', 'T05:00:00', 'T06:00:00', 'T07:00:00']
interval = map(convertToTimestamp, hours)

temperatures = []

for time in times:
    if time['@from'] in interval:
        temperatures.append(time['temperature']['@value'])

def belowFreezingPoint(temperature):
    return temperature <= 0

# If the temperature is less than or equal to 0 degrees celcius, trigger notification
degreesBelowFreezing = filter(belowFreezingPoint, temperatures)

slack = Slack(env.get('SLACK_API_TOKEN'), env.get('SLACK_CHANNEL'))

if len(degreesBelowFreezing):
    slack.send_message(str(min(degreesBelowFreezing)))
elif env.get('DEBUG', False):
    slack.send_message('-100')
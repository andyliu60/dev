#! /usr/bin/python
import requests
import sys
from ifttt import Notification

url = ('api.recognition.microsoft.com', 'v1', 'user', 'a4985d59-80ff-4f5a-bcc1-3fa87467384a', 'stats?locale=en-US')
url_points = 'https://' + '/'.join(url[0:4])
url_answers = 'https://' + '/'.join(url)
forum_event = 'op-mark'

r_points = requests.get(url_points)
d_answers = requests.get(url_answers)
d_points = r_points.json()
d_answers = d_answers.json()
points = d_points["Points"]
answers = d_answers['Groups'][0]['Statistics'][0]['Value']

Notification(value1 = points, value2 = answers, event = forum_event).sent()




# -*- coding: utf-8 -*-
import requests

class Notification:
    
    mykey = 'dVNxHrwtqldbtVk8OjbsDs'
    def __init__(self, event, **values):
        self.url = "https://maker.ifttt.com/trigger/" + event + "/with/key/" + self.mykey
        self.report = values

    def sent(self):
        requests.post(self.url, data=self.report)

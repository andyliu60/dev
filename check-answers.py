#! /usr/bin/python
import requests
from bs4 import BeautifulSoup
import lxml
from urllib import urlopen
from ifttt import Notification
from datetime import datetime

url = "http://social.technet.microsoft.com/Profile/u/activities/feed?displayName=Andy%20Liu50"

def get_answered_threads():

    rss = urlopen(url)
    threads = {}
    titles = []
    links = []
    pub_date = []
    update_date = []
    rss_activities = urlopen(url)
    bsObj = BeautifulSoup(rss_activities, 'xml')

def format_datetime(dt):
    
    formatted_dt = dt.strip('Z').replace('T', ' ')

def filter_answered_threads():
    pass



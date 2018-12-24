#! /usr/bin/python
import requests
from bs4 import BeautifulSoup
import lxml
from urllib import urlopen
from ifttt import Notification
from datetime import datetime

url = "http://social.technet.microsoft.com/Profile/u/activities/feed?displayName=Andy%20Liu50"

def get_answered_threads():

    now = datetime.now()
    rss = urlopen(url)
    threads = {}
    titles = []
    links = []
    pub_date = []
    update_date = []
    
    pass


def filter_answered_threads():
    pass



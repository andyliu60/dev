#! /usr/bin/python3
import requests
from bs4 import BeautifulSoup
import lxml
from urllib.request import urlopen
from ifttt import Notification
from datetime import datetime
import html
import shelve

url = "http://social.technet.microsoft.com/Profile/u/activities/feed?displayName=Andy%20Liu50"
rss_activities = urlopen(url)
rss_activities_bsObj = BeautifulSoup(rss_activities, 'xml')

filter_word1 = 'answered'
filter_word2 = 'Answered'

this_month = datetime.now().month
s = shelve.open('check-answers', writeback=True)
if 'last_sync_time' not in s:
    raw_last_sync_time = rss_activities_bsObj.find("lastBuildDate").get_text().strip(' Z')
    last_sync_time = datetime.strptime(raw_last_sync_time, '%a, %d %b %Y %H:%M:%S').timestamp()
    s['last_sync_time'] = str(last_sync_time)
    print(raw_last_sync_time)
    print(last_sync_time)
    

def get_new_threads():
    updated_datetimes = rss_activities_bsObj.findAll("a10:updated")
    for updated_datetime in updated_datetimes:
        formatted_datetime = updated_datetime.get_text().strip('Z').replace('T', ' ')
        updated_time = datetime.strptime(formatted_datetime, '%Y-%m-%d %H:%M:%S').timestamp()
        if updated_time == float(s['last_sync_time']):
            new_threads_bsObj = updated_datetime.parent.previous_siblings
            break

    return new_threads_bsObj                     

def get_create_time(link):
    thread_content = urlopen(link)
    thread_content_bsObj = BeautifulSoup(thread_content, "lxml")
    raw_create_time = thread_content_bsObj.find("div", {"class":"date"})
    create_time = datetime.strptime(raw_create_time.get_text(), '%A, %B %d, %Y %H:%M %p')
    return create_time

def filter_threads():
    raw_new_threads = []
    intune_new_threads = []
    scvmm_new_threads = []
    mata_new_threads = []
    new_thread = {}
    
    raw_new_thread_items = get_new_threads()
    for raw_new_thread_item in raw_new_thread_items:
        if filter_word1 in raw_new_thread_item.get_text() or filter_word2 in raw_new_thread_item.get_text():
            raw_new_thread_item = raw_new_thread_item.find("description").get_text()
            raw_new_thread = html.unescape(raw_new_thread_item)
            raw_new_threads.append(raw_new_thread)
            
    for new_thread_item in raw_new_threads:
        new_thread_item_bsObj = BeautifulSoup(new_thread_item, "lxml")
        thread_forum = new_thread_item_bsObj.findAll("a")[1].attrs['title']
        thread_title = new_thread_item_bsObj.find("a").attrs['title']
        thread_link = new_thread_item_bsObj.find("a").attrs['href']
        thread_create_time = get_create_time(thread_link)
        if thread_create_time.month == this_month:
            new_thread = {"title":thread_title, "link":thread_link, "forum":thread_forum}
            if 'Intune' in thread_forum:
                intune_new_threads.append(new_thread)
            if 'Virtual Machine Manager' in thread_forum:
                scvmm_new_threads.append(new_thread)
            if 'Microsoft Advanced Threat Analytics' in thread_forum:
                mata_new_threads.append(new_thread)

raw_last_sync_time = rss_activities_bsObj.find("lastBuildDate").get_text().strip(' Z')
last_sync_time = datetime.strptime(raw_last_sync_time, '%a, %d %b %Y %H:%M:%S').timestamp()
s['last_sync_time'] = str(last_sync_time)
s.close()

    


    



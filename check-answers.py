#! /usr/bin/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import lxml
from urllib.request import urlopen
from ifttt import Notification
from datetime import datetime
import html
import shelve

url = "https://social.technet.microsoft.com/Profile/u/activities/feed?displayName=Andy%20Liu50"
rss_activities = urlopen(url)
rss_activities_bsObj = BeautifulSoup(rss_activities, 'xml')
filter_word1 = 'answered'
filter_word2 = 'Answered'

this_month = datetime.now().month
s = shelve.open('check-answers', writeback=True)
#s['last_sync_time'] = 1544727439.0
if 'last_sync_time' not in s:
    raw_last_sync_time = rss_activities_bsObj.find("lastBuildDate").get_text().strip(' Z')
    last_sync_time = datetime.strptime(raw_last_sync_time, '%a, %d %b %Y %H:%M:%S').timestamp()
    s['last_sync_time'] = last_sync_time

if 'intune_marked_answers' not in s:
    s['intune_marked_answers'] = 0
    
if 'scvmm_marked_answers' not in s:
    s['scvmm_marked_answers'] = 0

if 'mata_marked_answers' not in s:
    s['mata_marked_answers'] = 0

current_time = datetime.now()
if current_time.day == 1 and current_time.hour == 0 and current_time.minute == 0:
    s['intune_marked_answers'] = 0
    s['scvmm_marked_answers'] = 0
    s['mata_marked_answers'] = 0

new_threads = {"intune":[],"scvmm":[],"mata":[]}

def get_new_threads():
    updated_datetimes = rss_activities_bsObj.findAll("a10:updated")
    for updated_datetime in updated_datetimes:
        formatted_datetime = updated_datetime.get_text().strip('Z').replace('T', ' ')
        updated_time = datetime.strptime(formatted_datetime, '%Y-%m-%d %H:%M:%S').timestamp()
        if updated_time == s['last_sync_time']:
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
                new_threads["intune"].append(new_thread)
                Notification(value1=thread_forum, value2=thread_title, value3=thread_link, event='op-answers').sent()
            if 'Virtual Machine Manager' in thread_forum:
                new_threads["scvmm"].append(new_thread)
                Notification(value1=thread_forum, value2=thread_title, value3=thread_link, event='op-answers').sent()
            if 'Microsoft Advanced Threat Analytics' in thread_forum:
                new_threads["mata"].append(new_thread)
                Notification(value1=thread_forum, value2=thread_title, value3=thread_link, event='op-answers').sent()

raw_last_sync_time = rss_activities_bsObj.find("lastBuildDate").get_text().strip(' Z')
last_sync_time = datetime.strptime(raw_last_sync_time, '%a, %d %b %Y %H:%M:%S').timestamp()

if s['last_sync_time'] != last_sync_time:
    filter_threads()
    s['intune_marked_answers'] += len(new_threads["intune"])
    s['scvmm_marked_answers'] += len(new_threads["scvmm"])
    s['mata_marked_answers'] += len(new_threads["mata"])
    s['last_sync_time'] = last_sync_time
    summary = "Intune: %d | SCVMM: %d | MATA: %d" % (s['intune_marked_answers'], s['scvmm_marked_answers'], s['mata_marked_answers'])
    Notification(value1 = summary, event = 'mark-summary').sent()

s.close()

    


    



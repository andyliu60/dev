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
import time
import feedparser

url = "https://social.technet.microsoft.com/Profile/u/activities/feed?displayName=Andy%20Liu50"
d = feedparser.parse(url)
filter_word1 = 'answered'
filter_word2 = 'Answered'

this_month = datetime.now().month
s = shelve.open('check-answers', writeback=True)

#s['last_sync_time'] = 1544727439.0
#s['last_sync_time'] = 1545866100.0

if 'last_sync_time' not in s:
    last_sync_time = time.mktime(d.feed.updated_parsed)
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
    for index, entry in enumerate(d.entries):
        if time.mktime(entry.published_parsed) == s['last_sync_time']:
            new_entries = d.entries[0:index]
    
    return  new_entries
                 
def get_create_time(link):
    thread_content = urlopen(link)
    thread_content_bsObj = BeautifulSoup(thread_content, "lxml")
    raw_create_time = thread_content_bsObj.find("div", {"class":"date"})
    create_time = datetime.strptime(raw_create_time.get_text(), '%A, %B %d, %Y %H:%M %p')
    return create_time

def filter_threads():
    new_thread = {}
    raw_new_threads = []
    raw_new_entries = get_new_threads()
    
    for raw_new_entry in raw_new_entries:
        if filter_word1 in raw_new_entry.title or filter_word2 in raw_new_entry.title:
            raw_new_threads.append(raw_new_entry)
        
    if bool(raw_new_threads) == False:
        return None
    else:
        for raw_new_thread in raw_new_threads:
            item_description = html.unescape(raw_new_thread.description)
            item_description_bsObj = BeautifulSoup(item_description, "lxml")
            thread_forum = item_description_bsObj.findAll("a")[1].attrs['title']
            thread_title = item_description_bsObj.find("a").attrs['title']
            thread_link = item_description_bsObj.find("a").attrs['href']
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
        
        return raw_new_threads

                    
last_sync_time = time.mktime(d.feed.updated_parsed)

if s['last_sync_time'] != last_sync_time: 
    ft = filter_threads()
    s['last_sync_time'] = last_sync_time
    if bool(ft) == False:
        pass
    else:
        s['intune_marked_answers'] += len(new_threads["intune"])
        s['scvmm_marked_answers'] += len(new_threads["scvmm"])
        s['mata_marked_answers'] += len(new_threads["mata"])
        summary = "Intune: %d | SCVMM: %d | MATA: %d" % (s['intune_marked_answers'], s['scvmm_marked_answers'], s['mata_marked_answers'])
        Notification(value1 = summary, event = 'mark-summary').sent()

s.close()

    


    



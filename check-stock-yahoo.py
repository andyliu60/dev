#!/usr/bin/python3
# -*- coding: utf-8 -*-

import fix_yahoo_finance as yf
from ifttt import Notification
from datetime import datetime,timedelta

if datetime.now().weekday() == 0:
    days_back = 3
else:
    days_back= 3

start_date = datetime.now() - timedelta(days_back)

yhcs_event = 'yhcs_close'
yhcs_df = yf.download('601933.SS', start_date)
yhcs_close = yhcs_df.Close[1]
yhcs_previous_close = yhcs_df.Close[0]
yhcs_change = '%+.2f%%' % ((round((yhcs_close-yhcs_previous_close)/yhcs_previous_close, 4))*100)
Notification(value1 = yhcs_close, value2 = yhcs_change, event = yhcs_event).sent()

dhgf_event = 'dhgf_close'
dhgf_df = yf.download('002236.SZ', start_date)
dhgf_close = dhgf_df.Close[1]
dhgf_previous_close = dhgf_df.Close[0]
dhgf_change = '%+.2f%%' % ((round((dhgf_close-dhgf_previous_close)/dhgf_previous_close, 4))*100)
Notification(value1 = dhgf_close, value2 = dhgf_change, event = dhgf_event).sent()


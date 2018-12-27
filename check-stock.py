#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import tushare as ts
from ifttt import Notification
from datetime import datetime

token = ''

pro = ts.pro_api(token)

yhcs = '601933.SH'
dhgf = '002236.SZ'
yhcs_event = 'yhcs_close'
dhgf_event = 'dhgf_close'

today = datetime.now().day

yhcs_df = pro.daily(ts_code=yhcs)
dhgf_df = pro.daily(ts_code=dhgf)
yhcs_trade_day = datetime.strptime(yhcs_df.trade_date[0], '%Y%m%d').day
dhgf_trade_day = datetime.strptime(dhgf_df.trade_date[0], '%Y%m%d').day

if yhcs_trade_day != today:
    Notification(value1 = '数据没有更新', event = yhcs_event).sent()

else:
    
    yhcs_price = yhcs_df.close[0]
    yhcs_pchange = '%+.2f%%' % round(yhcs_df.pct_chg[0],4)
    Notification(value1 = '收盘价：%.2f' % yhcs_price, value2 = '涨跌幅：' + yhcs_pchange, event = yhcs_event).sent()

if dhgf_trade_day != today:
    Notification(value1 = '数据没有更新', event = dhgf_event).sent()

else:
    
    dhgf_price = dhgf_df.close[0]
    dhgf_pchange = '%+.2f%%' % round(dhgf_df.pct_chg[0],4)
    Notification(value1 = '收盘价：%.2f' % dhgf_price, value2 = '涨跌幅：' + dhgf_pchange, event = dhgf_event).sent()

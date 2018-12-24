#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import tushare as ts
from ifttt import Notification

token = ''

pro = ts.pro_api(token)

yhcs = '601933.SH'
dhgf = '002236.SZ'
yhcs_event = 'yhcs_close'
dhgf_event = 'dhgf_close'

yhcs_df = pro.daily(ts_code=yhcs)
yhcs_price = yhcs_df.close[0]
yhcs_pchange = '%+.2f%%' % round(yhcs_df.pct_chg[0],4)

dhgf_df = pro.daily(ts_code=dhgf)
dhgf_price = dhgf_df.close[0]
dhgf_pchange = '%+.2f%%' % round(dhgf_df.pct_chg[0],4)

Notification(value1 = yhcs_price, value2 = yhcs_pchange, event = yhcs_event).sent()
Notification(value1 = dhgf_price, value2 = dhgf_pchange, event = dhgf_event).sent()

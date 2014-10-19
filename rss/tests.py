from django.test import TestCase
from django.utils import http
import requests

# Create your tests here.
'''
Created on 2014年9月16日

@author: shengeng
'''

def test_get_refresh_tlquan_news():
    url = 'http://localhost:8000/rss/refresh_tlquan_news/'
    #loginurl = 'http://www.yangwabao.com:80/user/login/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    r = requests.get(url, headers = headers)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    return r.text


test_get_refresh_tlquan_news()

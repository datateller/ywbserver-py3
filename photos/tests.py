from django.test import TestCase
from django.utils import http
import requests

def testuploadhead():
    username = 'shentest04'
    password = 'shentest04'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    babyname = 'shenruyi'
    babyheight = 1.4
    babyweight = 34
    birthday = '2012-04-08'
    babysex = 'girl'
    homeaddr = '北京市海淀区紫金庄园'
    schooladdr = '北京市万泉河路小学'
    #files = {'file': open('/home/lyb/sjzl.mpg', 'rb')}
    head = open('head.jpg', 'rb')
    files = {'head' : head}
    url = 'http://localhost:8000/photos/uploadhead/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password, 'babyname': babyname,
               'babyheight':babyheight, 'babyweight':babyweight, 'birthday':birthday,
               'babysex':babysex, 'homeaddr':homeaddr, 'schooladdr':schooladdr}
    #r = requests.post(url, data=payload, headers = headers, files = files)
    r = requests.post(url, data = payload, files = files)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    
testuploadhead()
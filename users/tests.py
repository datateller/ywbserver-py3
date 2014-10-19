"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

# from django.test import TestCase
# 
# 
# class SimpleTest(TestCase):
#     def test_basic_addition(self):
#         """
#         Tests that 1 + 1 always equals 2.
#         """
#         self.assertEqual(1 + 1, 2)

from django.utils import http
import requests

def testregister():
    username = 'sg8'
    password = 'sg8'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    babyname = 'ruyi01'
    babyheight = 1.4
    babyweight = 34
    birthday = '2013-05-05'
    babysex = 'girl'
    homelng = '116.30799772131'
    homelat = '39.971353229973'
    schoollng = '116.30799772131'
    schoollat = '39.971353229973'
    homeaddr = '北京市用友软件园'
    schooladdr = '北京市万泉庄小学'
    url = 'http://localhost:8000/user/register/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    #payload = {'username': username, 'password': password, 'babyname': babyname,
    #           'babyheight':babyheight, 'babyweight':babyweight, 'birthday':birthday,
    #         'babysex':babysex, 'homeaddr':homeaddr, 'schooladdr':schooladdr}
#     payload = {'username': username, 'password': password, 'babyname': babyname,
#                'birthday':birthday, 'homeaddr':homeaddr, 'schooladdr':schooladdr}
    payload = {'username': username, 'password': password, 'babyname': babyname,
               'birthday':birthday, 'homelng':homelng, 'homelat':homelat, 'schoollng':schoollng, 'schoollat':schoollat}
    r = requests.post(url, data=payload, headers = headers)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    return r.text
    
def testupdate():
    username = 'sg8'
    password = 'sg8'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    babyname = 'shenruyi2'
    babyheight = 1.4
    babyweight = 34
    birthday = '2012-08-08'
    babysex = 'girl'
    #homeaddr = '湖南省长沙市黄兴南路'
    homeaddr = '北京市海淀区紫金庄园'
    schooladdr = '北京市万泉河路小学'
    schoollng = '116.31789772131'
    schoollat = '39.971353229973'
    url = 'http://localhost:8000/user/update/'
    loginurl = 'http://localhost:8000/user/login/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(loginurl, data=payload, headers = headers)
    cookies = r.cookies
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = { 'babyname': babyname,
               'babyheight':babyheight, 'babyweight':babyweight, 'birthday':birthday,
               'babysex':babysex, 'schoollng':schoollng, 'schoollat':schoollat}
    r = requests.post(url, data=payload, headers = headers, cookies = cookies)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    return r.text
    
    
def testgetinfo():
    username = 'shentest1'
    password = 'shentest1'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    loginurl = 'http://localhost:8000/user/login/'
    url = 'http://localhost:8000/user/info/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(loginurl, data=payload, headers = headers)
    cookies = r.cookies
    print(cookies)
    r = requests.get(url, headers = headers, cookies=cookies)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    return r.text
    
def testuploadhead():
    username = 'shentest1'
    password = 'shentest1'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    loginurl = 'http://localhost:8000/user/login/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(loginurl, data=payload, headers = headers)
    cookies = r.cookies
    head = open('head.jpg', 'rb')
    files = {'portrait' : head}
    url = 'http://localhost:8000/user/posthead/'
    headers = {'content-Type': 'application/octet-stream'}
    payload = {'username': username, 'password': password}
    r = requests.post(url, data = payload, files = files, cookies = cookies)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    return r.text
    
def testgethead():
    username = 'sg'
    password = 'sg'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    loginurl = 'http://www.yangwabao.com:80/user/login/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(loginurl, data=payload, headers = headers)
    cookies = r.cookies
    url = 'http://www.yangwabao.com:80/user/gethead/?type=orig'
    r = requests.get(url,cookies = cookies)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    return r.text
    
#print(testuploadhead())
#print(testgethead()) 
#print(testgetinfo())
print(testupdate())
#print(testregister())
#print(testupdate())
#print(testinformationcheck())
#print(testregister())


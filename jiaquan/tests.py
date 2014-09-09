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

def test_post_topic():
    username = 'sg6'
    password = 'sg6'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    loginurl = 'http://localhost:8000/user/login/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(loginurl, data=payload, headers = headers)
    cookies = r.cookies
    content = '呵呵，测试发帖位置。'
    photo = open('photo.jpg', 'rb')
    files = {'photo' : photo}
    #url = 'http://www.yangwabao.com/jiaquan/posttopic/'
    url = 'http://localhost:8000/jiaquan/posttopic/'
    payload = {'username': username, 'password': password, 'content': content}
    r = requests.post(url, data=payload,  files = files, cookies = cookies)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    return r.text

def test_add_comment():
    username = 'shentest1'
    password = 'shentest1'
    topicid = 6
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    comment = '呵呵，测试一下在圈子里发个评论呗aaa。'
    url = 'http://localhost:8000/jiaquan/addcomment/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password, 'topicid':topicid, 'comment':comment}
    r = requests.post(url, data=payload, headers = headers)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()

def test_get_topiclist():
    username = 'shentest1'
    password = 'shentest1'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    loginurl = 'http://localhost:8000/user/login/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(loginurl, data=payload, headers = headers)
    cookies = r.cookies
    url = 'http://localhost:8000/jiaquan/listtopic/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    r = requests.get(url, data=payload, headers = headers, cookies = cookies)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    return r.text

def test_get_topiclist_nearby():
    username = 'shentest1'
    password = 'shentest1'
    latitude = '40.2160642139'
    longitude = '116.2098309870'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    loginurl = 'http://localhost:8000/user/login/'
    #loginurl = 'http://www.yangwabao.com:80/user/login/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(loginurl, data=payload, headers = headers)
    cookies = r.cookies
    url = 'http://localhost:8000/jiaquan/listtopicnearby/?page=1&number=2'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'latitude': latitude, 'longitude': longitude, 'page':1, 'number':5}
    r = requests.get(url, data=payload, headers = headers, cookies = cookies)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    return r.text

def test_get_topic():
    username = 'shentest1'
    password = 'shentest1'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    url = 'http://localhost:8000/jiaquan/getcircletopic/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(url, data=payload, headers = headers)
    print(r.text)
    fp = open("test_gettopic.html",'w')
    fp.write(r.text)
    fp.close()
    
def test_get_topic_webview():
    username = 'shentest2'
    password = 'shentest2'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    url = 'http://localhost:8000/jiaquan/gettopicwebview/14/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.get(url)
    fp = open("test_gettopic.html",'w')
    fp.write(r.text)
    fp.close()

def test_get_topicbyid_webview():
    username = 'shentest2'
    password = 'shentest2'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    url = 'http://localhost:8000/jiaquan/gettopicwebview/14/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.get(url)
    fp = open("test_gettopic.html",'w')
    fp.write(r.text)
    fp.close()

def test_post_comment():
    username = 'sg6'
    password = 'sg6'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    loginurl = 'http://localhost:8000/user/login/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(loginurl, data=payload, headers = headers)
    cookies = r.cookies
    content = '呵呵，测试post评论。'
    photo = open('photo.jpg', 'rb')
    files = {'photo' : photo}
    topicid = 1
    #url = 'http://www.yangwabao.com/jiaquan/posttopic/'
    url = 'http://localhost:8000/jiaquan/postcomment/'
    payload = {'username': username, 'password': password, 'content': content, 'topicid':topicid}
    r = requests.post(url, data=payload, cookies = cookies)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    return r.text

def test_collect():
    username = 'shentest1'
    password = 'shentest1'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    loginurl = 'http://localhost:8000/user/login/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(loginurl, data=payload, headers = headers)
    cookies = r.cookies
    url = 'http://localhost:8000/jiaquan/collect/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'id': 2}
    r = requests.post(url, data=payload, headers = headers, cookies = cookies)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    return r.text

def test_cancle_collect():
    username = 'shentest1'
    password = 'shentest1'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    loginurl = 'http://localhost:8000/user/login/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(loginurl, data=payload, headers = headers)
    cookies = r.cookies
    url = 'http://localhost:8000/jiaquan/cancel/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'id': 2}
    r = requests.post(url, data=payload, headers = headers, cookies = cookies)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    return r.text

def test_get_collect():
    username = 'shentest1'
    password = 'shentest1'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    loginurl = 'http://localhost:8000/user/login/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(loginurl, data=payload, headers = headers)
    cookies = r.cookies
    url = 'http://localhost:8000/jiaquan/listcollect/?number=3&page=0'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {}
    r = requests.get(url, data=payload, headers = headers, cookies = cookies)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    return r.text

#print(test_post_topic())
#print(test_add_comment())
#print(test_get_topic())
#print(test_get_topiclist())
#print(test_get_topiclist_nearby())
#print(test_get_topic_webview())
#print(test_post_comment())
#print(test_collect())
#print(test_get_collect())
print(test_cancle_collect())


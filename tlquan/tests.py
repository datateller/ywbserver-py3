
from django.utils import http
import requests

def test_post_topic():
    username = 'shentest1'
    password = 'shentest1'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    loginurl = 'http://localhost:8000/user/login/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(loginurl, data=payload, headers = headers)
    cookies = r.cookies
    content = '呵呵，发布图片试一下。'
    photo = open('photo.jpg', 'rb')
    files = {'photo' : photo}
    #url = 'http://www.yangwabao.com/jiaquan/posttopic/'
    url = 'http://localhost:8000/tlquan/posttopic/'
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
    #loginurl = 'http://www.yangwabao.com:80/user/login/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(loginurl, data=payload, headers = headers)
    cookies = r.cookies
    url = 'http://localhost:8000/tlquan/listtopic/?page=1&number=3'
    #url = 'http://www.yangwabao.com:80/tlquan/listtopic/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
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

#print(test_post_topic())
#print(test_add_comment())
#print(test_get_topic())
print(test_get_topiclist())
#print(test_get_topic_webview())

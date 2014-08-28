from django.utils import http
import requests

def testpublishfindhelp():
    username = 'shentest1'
    password = 'shentest1'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    loginurl = 'http://localhost:8000/user/login/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(loginurl, data=payload, headers = headers)
    cookies = r.cookies

    url = 'http://localhost:8000/merchant/publish_findhelp/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'content':"测试移动端帮你找修改后没有有效时间"}
    r = requests.post(url, data=payload, headers = headers, cookies = cookies)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    return r.text

def testpublishfindhelpvaliddate():
    username = 'shentest1'
    password = 'shentest1'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    loginurl = 'http://localhost:8000/user/login/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(loginurl, data=payload, headers = headers)
    cookies = r.cookies

    url = 'http://localhost:8000/merchant/publish_findhelp/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    #payload = {'content':"测试移动端帮你找有效时间", 'validdate':"2016-08-20"}
    payload = {'content':"测试移动端帮你找有效时间"}
    r = requests.post(url, data=payload, headers = headers, cookies = cookies)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    return r.text

def testrelatedmerchant():
    username = 'shentest1'
    password = 'shentest1'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    loginurl = 'http://localhost:80/user/login/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(loginurl, data=payload, headers = headers)
    cookies = r.cookies

    url = 'http://localhost:80/merchant/user_demand_related_merchant/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'content':"测试移动端帮你找修改后"}
    r = requests.get(url, data=None, headers = None, cookies = cookies)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    return r.text


def test_single_userdemand():
    username = 'shentest1'
    password = 'shentest1'
    username = http.urlsafe_base64_encode(username.encode()).decode()
    password = http.urlsafe_base64_encode(password.encode()).decode()
    loginurl = 'http://localhost:80/user/login/'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password}
    r = requests.post(loginurl, data=payload, headers = headers)
    cookies = r.cookies

    url = 'http://localhost:80/merchant/mobile_single_userdemand/?userdemandid=1'
    headers = {'content-Type': 'application/x-www-form-urlencoded'}
    payload = {'content':"测试移动端帮你找修改后"}
    r = requests.get(url, data=None, headers = None, cookies = cookies)
    fp = open("test.html",'w')
    fp.write(r.text)
    fp.close()
    return r.text

#print(testpublishfindhelp())
print("===========================")
print(testpublishfindhelpvaliddate())
print("===========================")
#print(test_single_userdemand())
#print(testrelatedmerchant())
# Create your tests here.

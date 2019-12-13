# import requests

# url = "http://127.0.0.1:8000/selectCourse/deleteCourse/"
# url2 = "http://127.0.0.1:8000/selectCourse/login/"

# payload = "course_id=000000"
# payload2 = "user_id=root&password=root"
# headers = {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
#     "Cache-Control": "max-age=0",
#     "Connection": "keep-alive",
#     "Host": "127.0.0.1:8000",
#     # "Sec-Fetch-Mode": "navigate",
#     # "Sec-Fetch-Site": "none",
#     # "Sec-Fetch-User": "?1",
#     # "Upgrade-Insecure-Requests": "1",
#     "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36"
#         }
        
#  headers=headers,
# requests.session['is_login'] = True
# requests.session['role'] = 0

# s = requests.Session()
# s.headers.update({'is_login':True,'role':0})
# response = requests.request("POST", url2, data=payload2, headers=headers)
# response = requests.post(url, headers=headers,data=payload)

# print(response.text)

# import http.client

# conn = http.client.HTTPConnection("127.0.0.1")

# payload = "course_id=ATMO130002&undefined="

# headers = {
#     'Content-Type': "application/x-www-form-urlencoded",
#     'cache-control': "no-cache",
#     'cache-control': "max-age=0",
#     'Postman-Token': "c77b92ec-9c2f-43be-8aa1-d29d867f9436",
#     "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
#     "Accept-Encoding": "gzip deflate,br",
#     "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
#     "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36",
#     "Connection": "keep-alive"
  

#     }

# conn.request("POST", "selectCourse,deleteCourse,", payload, headers)

# res = conn.getresponse()
# data = res.read()

# print(data.decode("utf-8"))

import requests

url = "http://127.0.0.1:8000/selectCourse/login/"

payload = "user_id=root&password=root"
headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache",
    'Postman-Token': "431ff01d-c29c-40c8-aba4-fed18346eb33"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
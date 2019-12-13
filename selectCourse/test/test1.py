import requests
import http.client
import unittest

BASE_URL = "http://127.0.0.1:8000/selectCourse/"

class SelectCourse(unittest.TestCase):
    # def test_delete_course(self):
    #     url = BASE_URL + "deleteCourse/"
    #     payload = "course_id=SSSS88888"

    #     headers = {
    #     'Content-Type': "application/x-www-form-urlencoded",
    #     'cache-control': "no-cache",
    #     'Postman-Token': "96d0f504-6cce-40fb-99d0-348a882dc477"
    #     }

     

    #     response = requests.request("POST",url=url,data=payload,headers=headers)

    #     print(response.text)
    #     self.assertEqual(response.status_code,200)
    #     # self.assertEqual(response['msg'],'')
    
    def test_delete(self):
        conn = http.client.HTTPConnection("127,0,0,1")

        payload = "course_id=ATMO130002&undefined="

        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache",
            'Postman-Token': "3584aae9-cefb-424b-a752-56a0d9329f47"
            }

        conn.request("POST", "selectCourse,deleteCourse,", payload, headers)

        res = conn.getresponse()
        data = res.read()

        print(data.decode("utf-8"))


if __name__ == '__main__':
    unittest.main()







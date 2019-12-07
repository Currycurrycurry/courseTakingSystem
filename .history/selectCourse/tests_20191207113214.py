from django.test import TestCase,Client
from django.core.serializers.json import DjangoJSONEncoder
import json
from selectCourse import models

def init_client(role):
    client = Client()
    s = client.session
    s['is_login'] = True
    s['role'] = role
    s.save()
    return client

class SelectCourseTestCase(TestCase):

    def setUp(self):
        # models.Account.objects.create(id=17302010063,password="17302010063",role=1)
        # models.Student.objects.create(student_id=17302010063)
        pass
    
    def test_login_ok(self):       
        c = Client()
        data = {'id':17302010015,'password':'17302010015'}
        response = c.post('/selectCourse/login/',data)
        print(response.content)
        self.assertEqual(response.status_code,200)
        # self

    # def test_write(self):
    #     c = Client()
    #     data = {'classroom_no':'Z9999','capacity':80}
    #     response = c.post('/selectCourse/write/',data)
    #     print(response.content)
    #     self.assertEqual(response.status_code,200)

    def test_read(self):
        c = Client();
        data = {'classroom_no':"Z2001"}
        response = c.get('/selectCourse/read/',data)
        print(response.content)
        self.assertEqual(response.status_code,200)



    # def test_login_wrong_usrid(self):
    #     c = Client()
    #     response = c.post('/login/',{'id':17302010062,'password':'17302010063'})
    #     self.assertEqual(response,status_code,200)

    # def test_login_wrong_passwd(self):
    #     c = Client()
    #     response = c.post('/login/',{'id':17302010063,'password':'17302010062'})
    #     self.assertEqual(response,status_code,200)

    # def test_select_course_ok(self):
    #     client = init_client(1)
    #     pass

    # def test_select_course_already_selected(self):
    #     client = init_client(1)
    #     pass

    # def test_select_course_no_vacancy(self):
    #     client = init_client(1)
    #     pass

    # def test_select_course_unauthorized(self):
    #     client = init_client(2)
    #     pass


    # def test_drop_course_ok(self):
    #     client = init_client(1)
    #     pass

    # def test_drop_course_not_take(self):
    #     client = init_client(1)
    #     pass

    # def test_drop_course_wrong_courseid(self):
    #     client = init_client(1)
    #     pass

    # def test_drop_course_unauthorized(self):
    #     pass
    
    # def test_checkCourseTable_ok(self):
    #     pass

    # def test_checkCourseTable_unauthorized(self):
    #     pass

    # def test_checkAllCourses_ok(self):
    #     pass

    # def test_checkAllCourses_unauthorized(self):
    #     pass

    # def test_checkPersonalInfo_ok(self):
    #     pass

    # def test_checkPersonalInfo_unauthorized(self):
    #     pass

    # def test_checkCourseNameList_ok(self):
    #     pass

    # def test_checkCourseNameList_unauthorized(self):
    #     pass

    # def handleApplication_pass(self):
    #     pass

    # def handleApplication_not_pass(self):
    #     pass

    # def handleApplication_unauthorized(self):
    #     pass

    # def applyCourse_ok(self):
    #     pass

    # def applyCourse_already_taken(self):
    #     pass

    # def applyCourse_already_applied(self):
    #     pass

    # def applyCourse_unauthorized(self):
    #     pass

    # def registerScore_ok(self):
    #     pass












        






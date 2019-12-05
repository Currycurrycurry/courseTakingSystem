from django.test import TestCase,Client

from selectCourse import models

def init_client_(role):
    client = Client()
    s = client.session
    s['is_login'] = True
    s['role'] = role
    s.save()
    return client

class SelectCourseTestCase(TestCase):

    def setUp(self):
        models.Account.objects.create(id=17302010063,password="17302010063",role=1)
    
    def test_login_ok(self):
        c = Client()
        response = c.post('/login/',{'id':17302010063,'password':'17302010063'})
        self.assertEqual(response,status_code,200)

    def test_login_wrong_usrid(self):
        c = Client()
        response = c.post('/login/',{'id':17302010062,'password':'17302010063'})
        self.assertEqual(response,status_code,200)

    def test_login_wrong_passwd(self):
        c = Client()
        response = c.post('/login/',{'id':17302010063,'password':'17302010062'})
        self.assertEqual(response,status_code,200)

  

    def test_select_course_ok(self):
        pass

    def test_select_course_already_selected(self):
        pass

    def test_select_course_no_vacancy(self):
        pass

    def test_select_course_unauthorized(self):
        pass


    def test_drop_course_ok(self):
        pass

    def test_drop_course_not_take(self):
        pass

    def test_drop_course_wrong_courseid(self):
        pass

    def test_drop_course_unauthorized(self):
        pass
    
    def test_checkCourseTable_ok(self):
        pass

    def test_checkCourseTable_unauthorized(self):
        pass

    def test_checkAllCourses_ok(self):
        pass

    def test_checkAllCourses_unauthorized(self):
        pass

    def test_checkPersonalInfo_ok(self):
        pass

    def test_checkPersonalInfo_unauthorized(self):
        pass

    def test_checkCourseNameList_ok(self):
        pass

    def test_checkCourseNameList_unauthorized(self):
        pass

    def handleApplication_pass(self):
        pass

    def handleApplication_not_pass(self):
        pass

    def handleApplication_unauthorized(self):
        pass

    def applyCourse_ok(self):
        pass

    def applyCourse_









        






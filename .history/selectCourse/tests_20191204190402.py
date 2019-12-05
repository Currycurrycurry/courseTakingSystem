from django.test import TestCase,Client

from selectCourse import models

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

    def init_client(user):
        client = Client()
        
        






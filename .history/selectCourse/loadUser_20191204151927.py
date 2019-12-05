from django.contrib.auth.models import User
from selectCourse import models

account = models.Account
user = User.objects.create_user(account.objects.all())


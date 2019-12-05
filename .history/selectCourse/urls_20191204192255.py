from django.urls import path
# from django.contrib import admin
from . import views
from selectCourse import views as server_views


urlpatterns = [
    # path('admin/',admin.site.urls),
    path('index/', views.index, name='index'),
    # path('write/',server_views.write_server),
    # path('read/',server_views.read_server),
    path('login/',views.login),
    path('logout/',views.logout),
    path('select/',views.selectCourse),
    path('dropCourse/',views.dropCourse),
    path('showCourses/',views.showCourses),
    path('showCourseTable/',views.showCourseTable),
    path('checkCourseTable/',views.checkCourseTable),
    path('checkAllCourses/',views.checkAllCourses),
    path('checkPersonalInfo/',views.checkPersonalInfo),
    path('checkCourseNameList',views.checkCourseNameList)
]


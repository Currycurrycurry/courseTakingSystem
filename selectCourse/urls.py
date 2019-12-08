from django.urls import path
# from django.contrib import admin
from . import views
from selectCourse import views as server_views


urlpatterns = [
    # path('admin/',admin.site.urls),
    path('index/', views.index, name='index'),
    # path('write/',server_views.write_server),
    # path('read/',server_views.read_server),
    path('login/',views.login_sql),
    path('logout/',views.logout),
    path('select/',views.select_sql),
    path('dropCourse/',views.dropCourse_sql),
    path('checkCourseTable/',views.checkCourseTable_sql),
    path('checkAllCourses/',views.checkAllCourses_sql),
    path('checkPersonalInfo/',views.checkPersonalInfo_sql),
    path('checkTaughtCourses/',views.checkTaughtCourses_sql),
    path('checkCourseNamelist/',views.checkCourseNamelist_sql),
    path('searchCourse/',views.searchCourse_sql),
    path('checkApplication/',views.checkApplication_sql),
    path('handleApplication/',views.handleApplication_sql),
    path('applyCourse/',views.applyCourse_sql),
    path('registerScore/',views.registerScore_sql),
    path('registerStudent/',views.registerStudent_sql),
    path('registerInstructor/',views.registerInstructor_sql),
    path('registerCourses/',views.registerCourses_sql),


]


from django.urls import path
# from django.contrib import admin
from . import views
from selectCourse import views
from selectCourse import service_view

urlpatterns = [
    # path('admin/',admin.site.urls),
    path('index/', views.index, name='index'),
    # path('write/',server_views.write_server),
    # path('read/',server_views.read_server),
    # path('login/',views.login_sql),
    # path('logout/',views.logout),
    # path('dropCourse/',views.dropCourse_sql),
    # path('checkCourseTable/',views.checkCourseTable_sql),
    # path('checkPersonalInfo/',views.checkPersonalInfo_sql),
    # path('checkTaughtCourses/',views.checkTaughtCourses_sql),
    # path('checkCourseNameList/',views.checkCourseNamelist_sql),
   

    # path('searchCourse/',views.searchCourse_sql),
    # path('checkApplication/',views.checkApplication_sql),
    # path('handleApplication/',views.handleApplication_sql),
    # path('applyCourse/',views.applyCourse_sql),
    # path('registerScore/',views.registerScore_sql),
    # path('registerStudent/',views.registerStudent_sql),
    # path('registerInstructor/',views.registerInstructor_sql),
    # path('registerCourses/',views.registerCourses_sql),

    path('login/',service_view.login),
    path('logout/',service_view.logout),
    path('select/',service_view.select),
    path('drop/',service_view.drop),
    path('checkCourseTable/',service_view.checkCourseTable),
    path('checkAllCourses/',service_view.checkAllCourses),
    path('checkExamTable/',service_view.checkExamTable),
    path('checkPersonalInfo/',service_view.checkPersonalInfo),
    path('checkTaughtCourses/',service_view.checkTaughtCourses),
    path('checkCourseNameList/',service_view.checkCourseNameList),
    path('search/',service_view.search),

    path('submitApplication/',service_view.submitApplication),
    path('checkApplications/',service_view.checkApplications),
    path('handleApplications/',service_view.handleApplication)


]


from django.urls import path
# from django.contrib import admin
from . import views
from selectCourse import views
from selectCourse import service_view

urlpatterns = [
    path('index/', views.index, name='index'),

    path('login/',service_view.login),
    path('logout/',service_view.logout),
################################################
    path('select/',service_view.select),
    path('drop/',service_view.drop),
################################################
    path('checkCourseTable/',service_view.checkCourseTable),
    # path('checkAllCourses/',service_view.checkAllCourses),
    path('checkExamTable/',service_view.checkExamTable),
    path('checkPersonalInfo/',service_view.checkPersonalInfo),
    path('checkTaughtCourses/',service_view.checkTaughtCourses),
    path('checkCourseNameList/',service_view.checkCourseNameList),

    ################################################
    path('search/',service_view.search),
################################################
    path('submitApplication/',service_view.submitApplication),
    path('checkApplications/',service_view.checkApplications),
    path('handleApplication/',service_view.handleApplication),

################################################v
    path('downloadFile/',service_view.downloadFile),
    
    path('registerStudent/',service_view.registerStudent),
    path('registerInstructor/',service_view.registerInstructor),
    path('registerStudent/',service_view.registerStudent),
    path('registerCourse/',service_view.registerCourse),


################################################################################################
    # only for root users
    path('deleteCourse/',service_view.deleteCourse),
    path('insertCourse/',service_view.insertCourse),
    path('checkCourses/',service_view.checkCourses),
    path('updateCourse/',service_view.updateCourse),

    path('deleteSection/',service_view.deleteSection),
    path('insertSection/',service_view.insertSection),
    path('checkSections/',service_view.checkSections),
    path('updateSection/',service_view.updateSection),

    path('deleteStudent/',service_view.deleteStudent),
    path('insertStudent/',service_view.insertStudent),
    path('updateStudent/',service_view.updateStudent),
    path('checkStudents/',service_view.checkStudents),


    path('deleteInstructor/',service_view.deleteInstructor),
    path('insertInstructor/',service_view.insertInstructor),
    path('updateInstructor/',service_view.updateInstructor),
    path('checkInstructors/',service_view.checkInstructors),
    
    
    path('updateExam/',service_view.updateExam),
    path('checkExams/',service_view.checkExams),
    path('insertExam/',service_view.insertExam),
    path('deleteExam/',service_view.deleteExam),

    path('insertClassroom/',service_view.insertClassroom),
    path('deleteClassroom/',service_view.deleteClassroom),
    path('checkClassrooms/',service_view.checkClassrooms),
    path('updateClassroom/',service_view.updateClassroom),

    path('insertAccount/',service_view.insertAccount),
    path('deleteAccount/',service_view.deleteAccount),
    path('updateAccount/',service_view.updateAccount),
    path('checkAccounts/',service_view.checkAccounts),

  


]


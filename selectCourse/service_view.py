from selectCourse.service.login_service import LoginService
from selectCourse.service.select_service import SelectService
from selectCourse.service.drop_service import DropService
from selectCourse.service.apply_service import ApplyService
from selectCourse.service.check_service import CheckService
from selectCourse.service.download_service import DownloadService
from selectCourse.service.import_service import ImportService
from selectCourse.service.search_service import SearchService
from selectCourse.service.root_service import RootService


############### Login SERVICE#####################
def login(request):
    return LoginService(request).execute()

def logout(request):
    return LoginService(request).logout()

######################################
def select(request):
    return SelectService(request).execute()

def drop(request):
    return DropService(request).execute()

######################################
def checkCourseTable(request):
    return CheckService(request).checkCourseTable()

def checkAllCourses(request):
    return CheckService(request).checkAllCourses()

def checkPersonalInfo(request):
    return CheckService(request).checkPersonalInfo()

def checkCourseNameList(request):
    return CheckService(request).checkCourseNameList()

def checkTaughtCourses(request):
    return CheckService(request).checkTaughtCourses()

def checkExamTable(request):
    return CheckService(request).checkExamTable()

######################################
def search(request):
    return SearchService(request).execute()

######################################
def submitApplication(request):
    return ApplyService(request).submitApplication()

def handleApplication(request):
    return ApplyService(request).handleApplication()

def checkApplications(request):
    return ApplyService(request).checkApplications()
    
######################################
def downloadFile(request):
    return DownloadService(request).execute()

############### IMPORT SERVICE############
def registerStudent(request):
    return ImportService(request).registerStudent()

def registerScore(request):
    return ImportService(request).registerCourse()

def registerInstructor(request):
    return ImportService(request).registerInstructor()

def registerCourse(request):
    return ImportService(request).registerCourse()


###############ROOT SERVICE########################
def deleteCourse(request):
    return RootService(request).deleteCourse()

def insertCourse(request):
    return RootService(request).insertCourse()

def checkCourses(request):
    return RootService(request).checkCourses()

def updateCourse(request):
    return RootService(request).updateCourse()
################################################
def deleteSection(request):
    return RootService(request).deleteSection()

def insertSection(request):
    return RootService(request).insertSection()

def checkSections(request):
    return RootService(request).checkSections()

def updateSection(request):
    return RootService(request).updateSection()
################################################
def deleteStudent(request):
    return RootService(request).deleteStudent()

def insertStudent(request):
    return RootService(request).insertStudent()

def updateStudent(request):
    return RootService(request).updateStudent()

def checkStudents(request):
    return RootService(request).checkStudents()
################################################


def deleteInstructor(request):
    return RootService(request).deleteInstructor()

def insertInstructor(request):
    return RootService(request).insertInstructor()

def updateInstructor(request):
    return RootService(request).updateInstructor()

def checkInstructors(request):
    return RootService(request).checkInstructors()
################################################
def updateExam(request):
    return RootService(request).updateExam()

def checkExams(request):
    return RootService(request).checkExams()

def insertExam(request):
    return RootService(request).insertExam()

def deleteExam(request):
    return RootService(request).deleteExam()
################################################
def insertClassroom(request):
    return RootService(request).insertClassroom()

def deleteClassroom(request):
    return RootService(request).deleteClassroom()

def checkClassrooms(request):
    return RootService(request).checkClassrooms()

def updateClassroom(request):
    return RootService(request).updateClassroom()

################################################

def insertAccount(request):
    return RootService(request).insertAccount()

def deleteAccount(request):
    return RootService(request).deleteAccount()

def updateAccount(request):
    return RootService(request).updateAccount()

def checkAccounts(request):
    return RootService(request).checkAccounts()









    
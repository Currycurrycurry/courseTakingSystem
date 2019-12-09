from selectCourse.service.login_service import LoginService
from selectCourse.service.select_service import SelectService
from selectCourse.service.drop_service import DropService
from selectCourse.service.apply_service import ApplyService
from selectCourse.service.check_service import CheckService
from selectCourse.service.download_service import DownloadService
from selectCourse.service.import_service import ImportService
from selectCourse.service.search_service import SearchService

def login(request):
    return LoginService(request).execute()

def logout(request):
    return LoginService(request).logout()

def select(request):
    return SelectService(request).execute()

def drop(request):
    return DropService(request).execute()

def apply(request):
    return ApplyService(request).execute()

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

def search(request):
    return SearchService(request).execute()

def submitApplication(request):
    return ApplyService(request).submitApplication()

def handleApplication(request):
    return ApplyService(request).handleApplication()

def checkApplications(request):
    return ApplyService(request).checkApplications()
    


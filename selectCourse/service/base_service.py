from django.http import JsonResponse

from selectCourse.logs import logger


class BaseService(object):
    def __init__(self,request):
        self.request = request
        self.response = {}

    def _init_response(self, status=None):
        if status and status["code"]:
            # self.response["result"] = False
            self.response["msg"] = status.get("msg", "")
            return
        elif status and status["code"] is None:
            self.response["msg"] = "invalid status"
            return
        self.response["msg"] = "success"

    def _get_response(self,msg=None,code=None):
        if msg != None:
            self.response["msg"] = msg
        if code != None:
            self.response["code"] = code
        return JsonResponse(self.response)

    def execute(self):
        logger.warning("[BaseService] method execute of BaseHandler should be implemented")
        pass

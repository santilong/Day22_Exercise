#Author:Santi
from django.shortcuts import HttpResponse
from django.utils.deprecation import MiddlewareMixin

# class Filterip(MiddlewareMixin):
#     def process_request(self,request):

class Row1(MiddlewareMixin):
    import re
    global p
    p = re.compile(r'17(\d+)')
    def process_request(self,request):
        ip = request.META['REMOTE_ADDR']
        m = p.search(ip)
        if m:
            # return HttpResponse('你的IP不允许登录')
            pass
        else:
            pass
    def process_response(self,request,response):
        # print('回来的最后一行')
        return response

class Row2(MiddlewareMixin):
    def process_request(self,request):
        # print('进去的第二行')
        pass
    def process_response(self,request,response):
        # print('回来的倒数第二行')
        return response

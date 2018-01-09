from django.shortcuts import render,redirect,HttpResponse

# Create your views here.

from django import forms
from django.forms import fields
from django.forms import widgets
from day22 import models

###通过session判断是否登录的装饰器
def checkSession(func):
    def inner(request,*args,**kwargs):
        try:
            stats = request.session['is_login']
            if not stats:
                return redirect('/login/')
            else:
                return func(request,*args,**kwargs)
        except KeyError as e:
            return redirect('/login/')
    return inner

class User(forms.Form):
    user = fields.CharField(
        max_length=12,
        min_length=3,
        widget=widgets.TextInput(attrs={'placeholder':'用户名','class':'form-control','id':'exampleInputEmail3'}),
        label="用户名：",
        error_messages={'required':'必填','max_length':'少于12个字符','min_length':'必须大于3个字符'}
    )
    pwd = fields.CharField(
        min_length=1,
        max_length=32,
        widget=widgets.PasswordInput(attrs={'placeholder':'','class':'form-control','id':'exampleInputPassword3'}),
        label="密码： ",
        error_messages={'required':'必填','min_length':'最少6个字符','max_length':'最大不超过32个字符'}
    )

def login(request):
    ret = {'error': None}
    if request.method == 'GET':
        obj = User()
        return render(request,'login.html',{'obj':obj})
    elif request.method == 'POST':
        obj = User(request.POST)
        check = obj.is_valid()
        # print(obj)
        postdata = obj.cleaned_data
        # print(postdata)
        result = models.user.objects.filter(username=postdata['user'],password=postdata['pwd']).first()
        r1 = models.user.objects.filter(username=postdata['user'])
        r2 = models.user.objects.filter(password=postdata['pwd'])
        r = request.POST.get('remember')
        # r = postdata['remember']
        if not r1 and not r2:
            ret['error'] = '账户和密码不存在'
        elif not r1 and r2:
            ret['error'] = '账户不存在'
        elif not r2 and r1:
            ret['error'] = '密码不正确'

        if check:
            if result:
                request.session['is_login'] = True
                request.session['username'] = postdata['user']
                if r == '1':
                    request.session.set_expiry(10000)
                else:
                    request.session.set_expiry(0)
                return redirect('/index/')
            else:
                obj = User()
                return render(request,'login.html',{'ret':ret,'obj':obj})
        else:
            return redirect('/login/')
@checkSession
def index(request):
    return render(request,'index.html',{'username':request.session['username']})

def logout(request):
    import json
    ret = {'logout':False,'error':None}
    if request.method == 'GET':
        return redirect('/index/')
    elif request.method == 'POST':
        status = request.POST.get('logout')
        if status == 'True':
            ret['logout'] = True
            # print(ret['logout'])
            request.session.clear()
        else:
            ret['error'] = '出错了'
    return HttpResponse(json.dumps(ret))

from day22.page import Page
@checkSession
def hosts(request):
    import json
    ret = {'status':True,'error':None,'data':None}
    get_ret = {'status':'0','error':None}
    try:
        if request.method == 'GET':
            obj = models.hosts.objects.all() ###列表
            current_page = request.GET.get('p', 1) ###分页的一切都基于p这个字符(也可以是其他字符)进行数据切割。设置当前页变量，如果没有，默认为1
            current_page = int(current_page)
            page = Page(current_page,len(obj))
            count = page.count
            if not count:
                count = 1
            if current_page > count:  ###如果当前页大于总页数，则返回第一页
                get_ret['status'] = '1'
                get_ret['error'] = '未找到该页'
                return render(request,'hosts.html',{'get_ret':get_ret})
            start = page.start  ###按页数切割数据，如果是第一页，则start为0，第二页，start为10，以此类推
            end = page.end  ###按页数切割数据，如果是第一页，end为10，第二页，end为20，以此类推
            obj = obj[start:end]  ###将获取的数据切片分个成按每页
            page_str = page.page_str()
            return render(request,'hosts.html',{'obj':obj,'page_str':page_str})
        elif request.method == 'POST':
            nid = request.POST.get('nid') ###获取每行信息在数据库中的ID
            if not nid:
                ret['status'] = False
                ret['error'] = '未找到指定的id'
            else:
                models.hosts.objects.filter(id=nid).delete()
    except Exception as e:
        print(e)
        ret['status'] = False
        ret['error'] = '出错了'
    return HttpResponse(json.dumps(ret))



class HostsInfo(forms.Form):
    # instanceid = fields.CharField(
    #     label="InstanceID：",
    #     min_length=3,
    #     max_length=32,
    #     widget=widgets.TextInput(attrs={'class':'form-control','style':'width:50%;'}),
    #     error_messages={'required':'必填','min_length':'大于3个字符','max_length':'小于32个字符'}
    # )
    hostname = fields.CharField(
        label='Hostname：',
        min_length=5,
        max_length=32,
        widget = widgets.TextInput(attrs={'class':'form-control','style':'width:50%;'}),
        error_messages ={'required':'必填','min_length':'大于5个字符','max_length':'小于32个字符'}
    )
    ip = fields.GenericIPAddressField(
        label='IP：',
        widget = widgets.TextInput(attrs={'class':'form-control','style':'width:50%;'}),
        error_messages ={'required':'必填','ip':'请输入可以的IP'}
    )
    port = fields.IntegerField(
        label='Port：',
        widget = widgets.TextInput(attrs={'class':'form-control','style':'width:50%;'}),
        error_messages ={'required':'必填'}
    )
@checkSession
def hostsedit(request,nid):
    info = models.hosts.objects.filter(id=nid)
    hostdic = {'id':info[0].id,'hostname':info[0].hostname,'ip':info[0].ip,'port':info[0].port}###通过查询querySet列表第一个元素获取queryset对象中的数据(hostname,ip,port)
    if request.method == 'GET':
        obj = HostsInfo(initial=hostdic)
        return render(request,'hostsedit.html',{'obj':obj,'nid':nid})
    elif request.method == 'POST':
        obj = HostsInfo(request.POST)
        check = obj.is_valid()
        # print(obj)
        if check:
            postdata = obj.cleaned_data
            # print(postdata)
            models.hosts.objects.filter(id=nid).update(**postdata)
        else:
            print(obj.errors.as_json)
            return render(request,'hostsedit.html',{'obj':obj})
    return render(request,'hostsedit.html')

@checkSession
def hostsadd(request):
    if request.method == 'GET':
        obj = HostsInfo()
        return render(request,'hostsadd.html',{'obj':obj})
    elif request.method == 'POST':
        obj = HostsInfo(request.POST)
        check = obj.is_valid()
        if check:
            data_dic = obj.cleaned_data
            print(data_dic)
            models.hosts.objects.create(**data_dic)
            return redirect('/hosts/')
        else:
            print(obj.errors.as_json)
            return render(request,'hostsadd.html',{'obj':obj})
    return redirect('/hosts/')
###增加AWS实例信息
# @checkSession
# def addAWSinstance(request):
#     from day22.dict import dic_list
#     for dic in dic_list:
#         models.hosts.objects.create(**dic)
#     print('数据创建完毕')
#     return redirect('/hosts/')

def test(request):
    import time
    t1 = time.time()
    t2 = time.time()
    t3 = time.time()
    return render(request,'test.html',{'t1':t1,'t2':t2,'t3':t3})
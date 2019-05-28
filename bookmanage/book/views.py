import json

from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpRequest
from django.urls import reverse

from .models import BookInfo,PeopleInfo
# Create your views here.



def wodemiddleware(request):
    print('我是中间键，我被调用啦')
    return HttpResponse('ok')



def indexmiddleware(request,value1,value2):
    print(123)
    print(value1,value2)
    context = {
        'name':[1,2,3]
    }
    return render(request,'book/inedx.html',context)
    # return redirect(reverse('book:index'))

def bookList(request):
    # a = request.POST.get('a')
    # b = request.POST.get('b')
    # alist = request.POST.getlist('a')
    # print(a)
    # print(b)
    # print(alist)
    # b_body = request.body
    # str_body = b_body.decode()
    # dic_body = json.loads(str_body)
    # print(dic_body.get('name'))
    # print(dic_body.get('age'))
    # print(dic_body['address'])
    # print(request.method)
    # print(request.path)
    # print(request.META['CONTENT_TYPE'])
    # print(request.META['CONTENT_LENGTH'])
    # print(request.META['HTTP_NAME'])
    # books = BookInfo.objects.all()
    # context = {
    #     'books':books
    # }
    print(reverse('book:index'))
    # return render(request,'book/inedx.html',context)
    response = HttpResponse('ok')
    response.set_cookie('name','wujg',max_age=3600)
    response['itcast'] = 'python'
    cook = request.COOKIES.get('name')
    print(cook)
    request.session['name'] = 'wijg'
    return response

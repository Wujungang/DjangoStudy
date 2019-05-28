import json
from django.views.generic import View
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpRequest,JsonResponse
from django.urls import reverse
from rest_framework.viewsets import ModelViewSet

from . import serializers
from .models import BookInfo,PeopleInfo
# Create your views here.


class BookInfoViewSet(ModelViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = serializers.BookInfoSerializer

class BookListView(View):
    def get(self,request):
        queryset = BookInfo.objects.all()
        book_list = []
        for book in queryset:
            book_list.append({
                'id':book.id,
                'name':book.name,
                'pub_date':book.pub_date
            })
        return JsonResponse(book_list,safe=False)

    def post(self,request):
        # book_dict = json.loads(request.body.decode())
        json_bytes = request.body
        json_str = json_bytes.decode()
        book_dict = json.loads(json_str)
        book = BookInfo.objects.create(
            name=book_dict.get('name'),
            pub_date = book_dict.get('pub_date')
        )
        return JsonResponse({
            'id':book.id,
            'name':book.name,
            'pub_date':book.pub_date
        },safe=False)

class BookDetailView(View):
    def get(self,request,id):
        try:
            book = BookInfo.objects.get(id=id)
        except Exception as e:
            return HttpResponse(e,status=404)
        return JsonResponse({
            'id':book.id,
            'name':book.name,
            'pub_date':book.pub_date
        })

    def put(self,request,id):
        try:
            book = BookInfo.objects.get(id=id)
        except Exception as e:
            return HttpResponse(e,status=404)
        book_dict = json.loads(request.body.decode())
        book.name = book_dict.get('name')
        book.pub_date = book_dict.get('pub_date')
        book.save()
        return JsonResponse({
            'id':book.id,
            'name':book.name,
            'pub_date':book.pub_date
        })

    def delete(self,request,id):
        try:
            book = BookInfo.objects.get(id=id)
        except Exception as e:
            return HttpResponse(e,status=404)
        book.delete()
        return HttpResponse(status=204)



#
# def wodemiddleware(request):
#     print('我是中间键，我被调用啦')
#     return HttpResponse('ok')
#
#
#
# def indexmiddleware(request,value1,value2):
#     print(123)
#     print(value1,value2)
#     context = {
#         'name':[1,2,3]
#     }
#     return render(request,'book/inedx.html',context)
#     # return redirect(reverse('book:index'))
#
# def bookList(request):
#     # a = request.POST.get('a')
#     # b = request.POST.get('b')
#     # alist = request.POST.getlist('a')
#     # print(a)
#     # print(b)
#     # print(alist)
#     # b_body = request.body
#     # str_body = b_body.decode()
#     # dic_body = json.loads(str_body)
#     # print(dic_body.get('name'))
#     # print(dic_body.get('age'))
#     # print(dic_body['address'])
#     # print(request.method)
#     # print(request.path)
#     # print(request.META['CONTENT_TYPE'])
#     # print(request.META['CONTENT_LENGTH'])
#     # print(request.META['HTTP_NAME'])
#     # books = BookInfo.objects.all()
#     # context = {
#     #     'books':books
#     # }
#     print(reverse('book:index'))
#     # return render(request,'book/inedx.html',context)
#     response = HttpResponse('ok')
#     response.set_cookie('name','wujg',max_age=3600)
#     response['itcast'] = 'python'
#     cook = request.COOKIES.get('name')
#     print(cook)
#     request.session['name'] = 'wijg'
#     return response

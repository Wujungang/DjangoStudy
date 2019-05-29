import json
from django.views.generic import View
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpRequest,JsonResponse
from django.urls import reverse
from rest_framework import status
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from . import serializers
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, \
    RetrieveUpdateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.viewsets import ViewSet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
#认证管理
from rest_framework.authentication import SessionAuthentication
#权限管理
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, BasePermission
from rest_framework.filters import OrderingFilter

from . import serializers
from .models import BookInfo,PeopleInfo
# Create your views here.

class BookDetailView(GenericAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = serializers.BookInfoSerializer
    throttle_classes = 'uploads'
    def get(self,request,pk):
        book = self.get_object()
        serializer = self.get_serializer(book)
        return Response(serializer.data)

class MyPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        """控制对obj对象的访问权限，此案例决绝所有对对象的访问"""
        return False

class BookListModelViewSet(ModelViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = serializers.BookInfoSerializer

    # authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny,MyPermission]

    #detail为True表示单个实例，网址为这种形式：^books/{pk}/set_bookname/$
    @action(methods=['post'], detail=True)
    def set_bookname(self, request, pk=None):
        book = self.get_object()
        serializer = serializers.BookInfoSerializer(data=request.data)
        if serializer.is_valid():
            book.name = request.data['name']
            book.save()
            return Response({'message': '重置成功'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    #detail为False表示列表，网址为这种形式：^books/order_comment/$
    @action(detail=False)
    def order_comment(self, request):
        books = BookInfo.objects.all().order_by('-commentcount')
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'p'
    page_query_param = 'ps'
    max_page_size = 10000

class BookViewSet(ModelViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = serializers.BookInfoSerializer
    throttle_classes = [AnonRateThrottle,UserRateThrottle]
    filter_fields = ['name']
    filter_backends = [OrderingFilter]
    ordering_fields = ['id','readcount']
    pagination_class = LargeResultsSetPagination
    # def list(self,request):
    #     queryset = BookInfo.objects.all()
    #     serializer = serializers.BookInfoSerializer(queryset,many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self,request,pk):
    #     queryset = BookInfo.objects.all()
    #     user = get_object_or_404(queryset,pk=pk)
    #     serializer = serializers.BookInfoSerializer(user)
    #     return Response(serializer.data)


class RetrieveUpdateDestoryView(RetrieveUpdateDestroyAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = serializers.BookInfoSerializer

class RetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = serializers.BookInfoSerializer

class DestoryView(DestroyAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = serializers.BookInfoSerializer

class RetrieveView(RetrieveAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = serializers.BookInfoSerializer

class ListView(ListAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = serializers.BookInfoSerializer
    filter_fields = ['name','id']
    filter_backends = [OrderingFilter]
    ordering_fields = ['id', 'readcount']
    # pagination_class = LargeResultsSetPagination
    pagination_class = LimitOffsetPagination

class CreateView(CreateAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = serializers.BookInfoSerializer

class DestroyModelView(DestroyModelMixin,GenericAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = serializers.BookInfoSerializer
    def delete(self,request,pk):
        return self.destroy(request)

class UpdateModelView(UpdateModelMixin,GenericAPIView):
     queryset = BookInfo.objects.all()
     serializer_class =serializers.BookInfoSerializer
     def put(self,request,pk):
        return self.update(request)

class RetrieveModelView(RetrieveModelMixin,GenericAPIView):
    queryset = BookInfo.objects.all()
    serializer_class =serializers.BookInfoSerializer

    def get(self,request,pk):
        return self.retrieve(request)

class CreateModelView(CreateModelMixin,GenericAPIView):
    queryset = BookInfo.objects.all()
    serializer_class =serializers.BookInfoSerializer

    def post(self,request):
        return self.create(request)

class ListModelView(ListModelMixin,GenericAPIView,):
    queryset = BookInfo.objects.all()
    serializer_class = serializers.BookInfoSerializer

    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self,request):
        return self.list(request)



#
# class BookListView(APIView):
#     def get(self,request):
#         books = BookInfo.objects.all()
#         serializer = serializers.BookInfoSerializer(books,many=True)
#         return Response(serializer.data)
#
# class BookInfoViewSet(ModelViewSet):
#     queryset = BookInfo.objects.all()
#     serializer_class = serializers.BookInfoSerializer
#
# class BookListView(View):
#     def get(self,request):
#         queryset = BookInfo.objects.all()
#         book_list = []
#         for book in queryset:
#             book_list.append({
#                 'id':book.id,
#                 'name':book.name,
#                 'pub_date':book.pub_date
#             })
#         return JsonResponse(book_list,safe=False)
#
#     def post(self,request):
#         # book_dict = json.loads(request.body.decode())
#         json_bytes = request.body
#         json_str = json_bytes.decode()
#         book_dict = json.loads(json_str)
#         book = BookInfo.objects.create(
#             name=book_dict.get('name'),
#             pub_date = book_dict.get('pub_date')
#         )
#         return JsonResponse({
#             'id':book.id,
#             'name':book.name,
#             'pub_date':book.pub_date
#         },safe=False)
#
# class BookDetailView(View):
#     def get(self,request,id):
#         try:
#             book = BookInfo.objects.get(id=id)
#         except Exception as e:
#             return HttpResponse(e,status=404)
#         return JsonResponse({
#             'id':book.id,
#             'name':book.name,
#             'pub_date':book.pub_date
#         })
#
#     def put(self,request,id):
#         try:
#             book = BookInfo.objects.get(id=id)
#         except Exception as e:
#             return HttpResponse(e,status=404)
#         book_dict = json.loads(request.body.decode())
#         book.name = book_dict.get('name')
#         book.pub_date = book_dict.get('pub_date')
#         book.save()
#         return JsonResponse({
#             'id':book.id,
#             'name':book.name,
#             'pub_date':book.pub_date
#         })
#
#     def delete(self,request,id):
#         try:
#             book = BookInfo.objects.get(id=id)
#         except Exception as e:
#             return HttpResponse(e,status=404)
#         book.delete()
#         return HttpResponse(status=204)



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

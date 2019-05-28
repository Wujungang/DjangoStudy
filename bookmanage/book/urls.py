from django.contrib import admin
from django.conf.urls import url,include
from rest_framework.routers import DefaultRouter
# from book.views import indexmiddleware, bookList,wodemiddleware

from . import views


router = DefaultRouter()
router.register(r'^books',views.BookInfoViewSet,)

urlpatterns = [
    url(r'^',include(router.urls)),
    # url(r'^books/(?P<id>\d+)',views.BookDetailView.as_view()),
    # url(r'^books/$',views.BookInfoViewSet.as_view(),name='index'),
]


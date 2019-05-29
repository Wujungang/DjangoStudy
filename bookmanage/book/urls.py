from django.contrib import admin
from django.conf.urls import url,include
# from book.views import indexmiddleware, bookList,wodemiddleware
from . import views
from rest_framework.routers import DefaultRouter,SimpleRouter
from rest_framework.documentation import include_docs_urls

router = DefaultRouter()
router.register(r'books',views.BookViewSet,base_name='')

urlpatterns = [
    url(r'^docs/', include_docs_urls(title='API接口文档')),
    # url(r'^',include(router.urls)),
    # url(r'^book/',views.BookListView.as_view(),name='index'),
    # url(r'^books/$',views.BookListView.as_view()),
    url(r'^books12/(?P<pk>\d+)/$',views.BookDetailView.as_view()),
    url(r'^books1/$',views.ListModelView.as_view()),
    url(r'^books2/$',views.CreateModelView.as_view()),
    url(r'^books3/(?P<pk>\d+)/$',views.RetrieveModelView.as_view()),
    url(r'^books4/(?P<pk>\d+)/$',views.UpdateModelView.as_view()),
    url(r'^books5/(?P<pk>\d+)/$',views.DestroyModelView.as_view()),
    url(r'^books6/$',views.CreateView.as_view()),
    url(r'^books7/$',views.ListView.as_view()),
    url(r'^books8/(?P<pk>\d+)/$',views.RetrieveView.as_view()),
    url(r'^books9/(?P<pk>\d+)/$',views.DestoryView.as_view()),
    url(r'^books10/(?P<pk>\d+)/$',views.RetrieveUpdateView.as_view()),
    url(r'^books11/(?P<pk>\d+)/$',views.RetrieveUpdateDestoryView.as_view()),

]
urlpatterns +=router.urls

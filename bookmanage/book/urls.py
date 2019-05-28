from django.contrib import admin
from django.conf.urls import url,include
from book.views import indexmiddleware, bookList,wodemiddleware

urlpatterns = [
    # url('admin/', admin.site.urls),
    url(r'^midd/$',wodemiddleware),
    url(r'^bookList/$',bookList,name='index'),
    url(r'^(?P<value1>\d+)/(?P<value2>\d+)/$',indexmiddleware)
]

from django.contrib import admin
from .models import BookInfo,PeopleInfo
from django.contrib import admin
# Register your models here.


# class PeopleInfoStackInLine(admin.StackedInline):
#     model = PeopleInfo #要关联的模型
#     extra = 2 #附加编辑的数量


class PeopleInfoTabularInline(admin.TabularInline):
    model = PeopleInfo #要关联的模型
    extra = 2 #附加编辑的数量

class BookInfoAdmin(admin.ModelAdmin):
    list_per_page = 2
    actions_on_top = True
    list_display = ['id','name','commentcount','readcount','bookname']
    list_filter = ['name','readcount']
    search_fields = ['name','id']
    fieldsets = (
        ('基本设置',{'fields':['name']}),
        ('高级设置',{'fields':['commentcount','readcount']}),
    )
    # inlines = [PeopleInfoStackInLine]
    inlines = [PeopleInfoTabularInline]

class PeopleInfoAdmin(admin.ModelAdmin):

    list_display = ['id','name','book','readcount','image','files']



admin.site.register(BookInfo,BookInfoAdmin)
admin.site.register(PeopleInfo,PeopleInfoAdmin)
admin.site.site_header = 'calis技术中心'#设置网站页头
admin.site.site_title = '管理中心'#设置页面标题
admin.site.index_title = '详情管理'#设置首页标语
# admin.site.register(BookInfo)
# admin.site.register(PeopleInfo)

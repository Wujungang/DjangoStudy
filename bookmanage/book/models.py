from django.db import models

# Create your models here.
# 准备书籍列表信息的模型类
class BookInfo(models.Model):
    # 创建字段，字段类型...
    name = models.CharField(max_length=20, verbose_name='名称')
    pub_date = models.DateField(verbose_name='发布日期',null=True)
    readcount = models.IntegerField(default=0, verbose_name='阅读量')
    commentcount = models.IntegerField(default=0, verbose_name='评论量')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')
    # data = models.DateField(auto_now=True,default='1994-94-94')
    class Meta:
        db_table = 'bookinfo'  # 指明数据库表名
        verbose_name = '图书'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name

    def __str__(self):
        """定义每个数据对象的显示信息"""
        return self.name

    def bookname(self):
        return '<<' + self.name + '>>'
    bookname.short_description = '书名'
    bookname.admin_order_field='name'
# 准备人物列表信息的模型类
class PeopleInfo(models.Model):
    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female')
    )
    name = models.CharField(max_length=20, verbose_name='名称')
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=0, verbose_name='性别')
    description = models.CharField(max_length=200, null=True, verbose_name='描述信息')
    book = models.ForeignKey(BookInfo, on_delete=models.CASCADE, verbose_name='图书')  # 外键
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')
    image = models.ImageField(upload_to='book',verbose_name='图片',null=True)
    files = models.FileField(upload_to='files',verbose_name='文件',null=True)
    class Meta:
        db_table = 'peopleinfo'
        verbose_name = '人物信息'
        #去除admin站点的名称的s后缀
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def readcount(self):
        return  self.book.readcount
    readcount.short_description='图书阅读量'
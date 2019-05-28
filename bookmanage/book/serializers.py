from rest_framework import serializers

from .models import BookInfo


# class BookInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BookInfo
#         fields = '__all__'

class BookInfoSerializer(serializers.Serializer):
    """图书数据序列化器"""
    id = serializers.IntegerField(label='ID', read_only=True)
    name = serializers.CharField(label='名称', max_length=20)
    pub_date = serializers.DateField(label='发布日期', required=False)
    readcount = serializers.IntegerField(label='阅读量', required=False)
    commentcount = serializers.IntegerField(label='评论量', required=False)
    image = serializers.ImageField(label='图片', required=False)
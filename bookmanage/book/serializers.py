from rest_framework import serializers

from .models import BookInfo


class BookInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInfo
        fields = '__all__'

class BookRelateField(serializers.RelatedField):
    """自定义用于处理图书的字段"""
    def to_representation(self, value):
        return 'Book: %d %s' % (value.id, value.name)


class BookInfoSerializer(serializers.Serializer):

    """图书数据序列化器"""
    id = serializers.IntegerField(label='ID', read_only=True)
    name = serializers.CharField(label='名称', max_length=20)
    pub_date = serializers.DateField(label='发布日期', required=False)
    readcount = serializers.IntegerField(label='阅读量', required=False)
    commentcount = serializers.IntegerField(label='评论量', required=False)
    image = serializers.ImageField(label='图片', required=False)
    peopleinfo_set = serializers.PrimaryKeyRelatedField(read_only=True, many=True)  # 新增


    def create(self, validated_data):
        """新建"""
        print(123)
        return BookInfo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """更新，instance为要更新的对象实例"""
        print(123)
        instance.name = validated_data.get('name', instance.name)
        instance.pub_date = validated_data.get('pub_date', instance.pub_date)
        instance.readcount = validated_data.get('readcount', instance.readcount)
        instance.commentcount = validated_data.get('commentcount', instance.commentcount)
        instance.save()
        return instance

class PeopleInfoSerializer(serializers.Serializer):
    """英雄数据序列化器"""
    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female')
    )
    id = serializers.IntegerField(label='ID', read_only=True)
    name = serializers.CharField(label='名字', max_length=20)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, label='性别', required=False)
    description = serializers.CharField(label='描述信息', max_length=200, required=False, allow_null=True)

    #外键显示为关联对象的id
    # book = serializers.PrimaryKeyRelatedField(label='图书', read_only=True)
    # book = serializers.PrimaryKeyRelatedField(label='图书',queryset=BookInfo.objects.all())
    #外键显示为关联对象的__str__ + readcount
    book = serializers.StringRelatedField(label='图书')
    #外键显示关联的序列化器
    # book = BookInfoSerializer()

    # 此字段将被序列化为获取关联对象数据的接口链接
    # book = serializers.HyperlinkedRelatedField(label='图书', read_only=True, view_name='book')


    # 此字段将被序列化为关联对象的指定字段数据
    # book = serializers.SlugRelatedField(label='图书', read_only=True, slug_field='pub_date')

    #自定义显示
    # book = BookRelateField(read_only=True)
#! usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2019/7/3
# Author: snow


from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from book_demo.models import *
from drf_yasg.utils import swagger_auto_schema, swagger_serializer_method
from django.db import connection
from django.core.paginator import Paginator
from django.db.utils import IntegrityError
# import pysnooper
import logging


logger = logging.getLogger(__name__)


class AuthorCreateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, help_text="作者姓名")
    age = serializers.IntegerField(required=False, help_text="年龄")
    authorDetail_id = serializers.IntegerField(required=False)


class AuthorReqSerializer(AuthorCreateSerializer):
    # todo 怎么只继承父类的个别属性，待确认
    nid = serializers.IntegerField(required=False, help_text="唯一ID")
    page = serializers.IntegerField(required=False)
    limit = serializers.IntegerField(required=False)


class DetailSerializer(serializers.Serializer):
    birthday = serializers.DateField()
    addr = serializers.CharField()


class AuthRespSerializer(serializers.Serializer):
    nid = serializers.IntegerField()
    name = serializers.CharField()
    authorDetail_id = serializers.IntegerField()
    telephone = serializers.SerializerMethodField()
    author_detail = serializers.SerializerMethodField()

    # 额外扩展：方式一
    @swagger_serializer_method(serializer_or_field=serializers.CharField)   # 里边类或实例都行
    def get_telephone(self, obj) -> str:
        """以 get_  开头的方法，用于指定其后字段的获取
            get_telephone  为  telephone字段的实现方法
        """
        return obj.authorDetail.telephone

    # 额外扩展：方式二
    @swagger_serializer_method(serializer_or_field=DetailSerializer)
    def get_author_detail(self, obj):
        detail_obj = AuthorDetail.objects.filter(nid=obj.nid).first()
        return DetailSerializer(detail_obj).data

    # 关于 serializers.DateField() 的注解
    # @swagger_serializer_method(serializer_or_field=serializers.CharField())
    # def get_birthday(self, obj) -> str:
    #     detail_obj = AuthorDetail.objects.filter(nid=obj.nid).first()
    #     # print(type(detail_obj.birthday))   # <class 'datetime.date'>  ，在sql中为Date类型
    #     """
    #     可以用datetime更mysql中date类型进行相互转化，但是不能直接将datetime对象加到sql中，可利用如下操作
    #         [in]: datetime.date(2019,1,2)
    #         [out]: datetime.date(2019, 1, 2)
    #
    #     sql_insert = "INSERT into tablename(exTime) values(str_to_date(\'%s\','%%Y-%%m-%%d %%H:%%i:%%s'))"
    #             %(dt.strftime("%Y-%m-%d %H:%M:%S"))
    #     """
    #     return detail_obj.birthday


class AuthorAllInfo(serializers.Serializer):
    """获取作者及其详情的所有信息，以及获取的总数量"""
    author_list = serializers.SerializerMethodField()
    total_count = serializers.IntegerField()

    @swagger_serializer_method(serializer_or_field=AuthRespSerializer)
    def get_author_list(self):
        return AuthRespSerializer().data


# ************************************************************************************************
class AuthorView(APIView):
    # @pysnooper.snoop(depth=2)
    @swagger_auto_schema(
        query_serializer=AuthorReqSerializer,
        responses={200: AuthorAllInfo},
        operation_summary="搜索作者信息, 接口摘要",
        operation_description="获取作者,接口内部描述信息",
        tags=["author  作者信息"]
    )
    def get(self, request, *args, **kwargs):
        """author get接口的描述"""
        req = request.query_params
        # print(req)  # <QueryDict: {'name': ['卡特'], 'age': ['16'], 'authorDetail': ['1']}>
        # print(type(req))  # <class 'django.http.request.QueryDict'>
        # print(req['age'])   # '234'
        # print(type(req['age']))   # <class 'str'>

        # if int(req["age"]) >= 20:
        #     author_obj_list = Author.objects.all()
        #     temp_serializer = AuthRespSerializer(instance=author_obj_list, many=True)
        #     return JsonResponse(temp_serializer.data, safe=False)
        # return JsonResponse(status=404, data={"code": "not_found_author_obj"})

        # print(req)  # <QueryDict: {'nid': ['2'], 'name': ['布隆', '卡特']}>
        # print(req.dict)  # <bound method MultiValueDict.dict of <QueryDict: {'nid': ['2'], 'name': ['布隆']}>>
        # print(type(req.dict))  # <class 'method'>

        req_dict =  {k:v for k, v in req.items()}   # 是个一键多值的对象，进行一次操作后，会自动取后者
        # print(req_dict)  # {'nid': '2', 'name': '卡特'}
        page = req_dict.pop("page", 1)
        limit = req_dict.pop("limit", 20)

        p = Paginator(Author.objects.filter(**req_dict).order_by("nid"), limit)
        resp = {
            "total_count": p.count,
            "author_list": AuthRespSerializer(p.get_page(page), many=True).data
        }
        # print(connection.queries)  # 查看执行的sql语句，以及运行时间
        """
        分页sql执行方式：
            - 1. count(*) 拿到总数量
            - 2. limit、ASC/DESC 拿到分页后的所有对象
            - 3. 根据对象取得关联表内相应的数据
        """
        return Response(resp)

    @swagger_auto_schema(
        request_body=AuthorCreateSerializer,
        responses={200: AuthRespSerializer},
        operation_description="创建作者详细",
        tags=["author  作者信息"],
        operation_summary="创建作者信息简介"
    )
    def post(self, request, *args, **kwargs):
        req_body = request.data
        # print(req_body)  # {'nid': 0, 'name': 'string', 'age': 0}
        try:
            author_obj = Author.objects.create(**req_body).save()
            print(author_obj)
            return Response(AuthRespSerializer(author_obj).data)
        except IntegrityError:
            # 这里有-对一关联
            return Response({"msg": "请先创建author_detai信息"}, 400)


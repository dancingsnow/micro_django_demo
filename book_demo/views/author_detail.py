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
from django.core.cache import cache
from micro_django_demo.utils.redis_cli import redis_client
import logging

logger = logging.getLogger(__name__)


# 方式二： 按需添加字段序列化
class AuthDetailReqSerializer(serializers.Serializer):
    """
    传递什么参数，则会接收到什么参数。flask-rest是没有的自动填None
    """
    birthday = serializers.DateField(required=False)
    telephone = serializers.CharField(required=False)
    addr = serializers.CharField(required=False)

class UpdateAuthorDetail(AuthDetailReqSerializer):
    nid = serializers.IntegerField(required=True)

# 方式一： model全字段序列化,请求，返回，皆可
class AuthDetailRespSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorDetail
        fields = "__all__"


class AuthDetailView(APIView):
    """作者详情"""
    @swagger_auto_schema(
        operation_description="详情",
        operation_summary="简介",
        query_serializer=AuthDetailReqSerializer,
        responses={200: AuthDetailRespSerializer},
        tags=["author_detail 作者详情标签"]
    )
    def get(self, request, *args, **kwargs):
        req = request.query_params
        # obj_list = AuthorDetail.objects.filter(**req).all()
        obj_list = AuthorDetail.objects.filter(**req)
        obj_list = obj_list.all()
        return Response(AuthDetailRespSerializer(obj_list, many=True).data)

    @swagger_auto_schema(
        operation_description="创建信息详情",
        operation_summary="创建简介",
        request_body=AuthDetailReqSerializer,
        responses={200: AuthDetailRespSerializer},
        tags=["author_detail 作者详情标签"]
    )
    def post(self, request, *args, **kwargs):
        req_body = request.data
        detail_obj = AuthorDetail.objects.create(**req_body)
        detail_obj.save()
        return Response(AuthDetailRespSerializer(detail_obj).data)
        # from django.http.response import JsonResponse, HttpResponse
        # return JsonResponse({"name": "lili"})
        # return HttpResponse("hahaha")

    @swagger_auto_schema(
        operation_description="修改信息详情",
        operation_summary="修改简介",
        request_body=UpdateAuthorDetail,
        responses={200: AuthDetailRespSerializer},
        tags=["author_detail 作者详情标签"]
    )
    def put(self, request, *args, **kwargs):
        req_body = request.data
        print(req_body)
        detail_obj = AuthorDetail.objects.filter(nid=req_body['nid']).first()
        if not detail_obj:
            return Response({"msg": "not_found_author_detail"}, 404)

        print(detail_obj)
        for k, v in req_body.items():
            setattr(detail_obj, k, v)
        detail_obj.save()
        # print(connection.queries)
        return Response(AuthDetailRespSerializer(detail_obj).data)

    @swagger_auto_schema(
        operation_description="删除信息详情",
        operation_summary="删除简介",
        query_serializer=UpdateAuthorDetail,
        responses={200: {}},
        tags=["author_detail 作者详情标签"]
    )
    def delete(self, request, *args, **kwargs):
        req = request.query_params
        print(req)
        detail_obj = AuthorDetail.objects.filter(nid=req['nid']).first()
        if not detail_obj:
            return Response({"msg": "not_found_author_detail"}, 404)
        detail_obj.delete()
        return Response({})
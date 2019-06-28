import calendar
import re
from datetime import date

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
# from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import *

User = get_user_model()


# TODO
# 1) get PK of Table instance from URL
# 2) pass the pk in get method as below and find Table instance with pk
# 3) returned Instance will delivered to Template we set above, and make the recipe Template
# 4) just Render with TemplateHTMLRenderer
# 5) make some update in Serializers.py
class RecipeEditorAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'editor.html'

    def get(self, request, pk):
        table = Table.objects.get(pk=pk)
        return Response({"table_code": table.recipe})

# 오늘의 식단 API
# class TodayTableAPI(generics.ListAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = TodayTableSerializer
#
#     def get_queryset(self):
#         queryset = cache.get('today_table')
#         if not queryset:
#             t_tables = TodayTable.objects.filter(
#                 date=date.today()
#             )
#             if not t_tables:
#                 return ""
#             cache.set('today_table', t_tables)
#             queryset = cache.get('today_table')

            ## queryset = TodayTable.objects.filter(
            ##     date=date.today()
                ## date__month=date.today().month,
                ## date__day=date.today().day
            ## )
         # return queryset


# 한상 식단 API
class TableListAPI(generics.ListAPIView):
    serializer_class = TableSerializer
    # queryset = Table.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = cache.get('table_list')
        if not queryset:
            tables = Table.objects.all()
            if not tables:
                return ""
            cache.set('table_list', tables)
            queryset = cache.get('table_list')
        return queryset

# TODO
# 이 달의 식단 > 이번 달 30일치의 식단을 전부?
# 그럼 중복 포함? or 제거?
# 한상 식단(전체 테이블 리스트)와의 차이?


# 이번 달의 식단 목록 불러오기(임시 API)
class MonthlyTableListAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TableSerializer

    def get_queryset(self):
        queryset = cache.get('monthly_table_list')
        if not queryset:
            monthrange = calendar.monthrange(date.today().year, date.today().month)
            from_date = date.today().replace(day=1)
            to_date = date.today().replace(day=monthrange[1])
            tables = Table.objects.filter(date__range=[from_date, to_date])
            if not tables:
                return ""
            cache.set('monthly_table_list', tables)
            queryset = cache.get('monthly_table_list')
        return queryset


# 한상식단 검색용 API
class TableSearchAPI(generics.ListAPIView):
    serializer_class = TableSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # parameter로 전달하는 방식
        if self.request.GET.get('keywords'):
            keywords = self.request.GET.get('keywords')
            queryset = Table.objects.filter(dietary_composition__icontains=keywords)
            return queryset
        else:
            return ""


# 메인페이지 API = 달력 + 섭취 기록(일주일 - 한 달)
class MainPageAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # 달력
        cal = calendar.monthrange(date.today().year, date.today().month)
        # 섭취 기록
        # Sample.objects.filter(date__range=["2011-01-01", "2011-01-31"]), time delta 사용

        user_monthly_log = TableLog.objects.filter(
            user=request.user,
            date__range=[date.today().replace(day=1), date.today().replace(day=cal[1])]
        )
        serializers = TableLogSerializer(user_monthly_log, many=True)
        # if serializers.is_valid(): > validated_data
        # 만약 is valid & validated data를 쓰는 경우, serializer에 넣을 때
        # data=[list] 로 파라미터를 넣어줘야만 한다.
        # 따라서 위 monthly log query도 list(query) 처리해줘야 한다.
        log_data = {
            "calendar": cal,
            "userLog": serializers.data
        }
        return Response(log_data, status=status.HTTP_200_OK)
        # return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


# class AddTableLogAPI(generics.CreateAPIView):
#     permission_classes = (IsAuthenticated,)
#
#     def perform_create(self, serializer):
#         TableLog.objects.create(
#             table__pk=serializer.validated_data["table_pk"],
#         )

class MakeTableLogAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = MakeTableLogSerializer(data=request.data)
        if serializer.is_valid():
            given_pk = serializer.validated_data["table_pk"]
            given_meal_time = serializer.validated_data["meal_time"]
            try:
                table_log = TableLog.objects.get(
                    user=request.user,
                    date=date.today(),
                    time=given_meal_time
                )
                table_log.table = Table.objects.get(pk=given_pk)
                table_log.save()
                return Response({
                    "message": "변경되었습니다.",
                    "tableLog": TableLogSerializer(table_log).data
                }, status=status.HTTP_202_ACCEPTED)

            except ObjectDoesNotExist:
                table_log = TableLog.objects.create(
                    table=Table.objects.get(pk=given_pk),
                    user=request.user,
                    date=date.today(),
                    time=given_meal_time
                )
                return Response(
                    {
                        "message": "저장되었습니다.",
                        "tableLog": TableLogSerializer(table_log).data
                     },
                    status=status.HTTP_201_CREATED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

import calendar
from datetime import date
from django.contrib.auth import get_user_model
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


class ExampleAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Table/example.html'

    def get(self, request):
        queryset = User.objects.all()
        return Response({"user_list": queryset})


# TODO
# 1) calendar.monthrange(2019, 5) > 달력
# 2) 클릭 > 식단 선택 > *오늘의 식단/한상식단 선택*
    # >> 오늘의 식단 불러오기(cashing 해둔 오늘의 식단 불러오기 > Redis 사용)
        # >> 오늘의 식단 : 식단 구성 / 레시피 / 영양정보 불러오기
    # >> 한상 식단 리스트 불러오기
        # >> 검색 기능 추가(Elastic Search 사용)
        # >> 식단 선택 시 한상 식단 : 식단 구성 / 레시피 / 영양정보 불러오기

# 3) 현재 이용 중인 특정 유저의 TableLog를 불러오기
    # >> 일주일 ~ 한달 간의 섭취 내역 불러오기
        # >> 테이블로그에서 유저 pk를 인덱스로 저장해둘 것

# API
# 1) + 3) 을 동시에 돌려주는 것이 Main Page API
# 2) Main Page에서 한상 식단 / 오늘의 식단 선택 시 이후 진행

# 캐싱 사용 > TodayTable / TableLog (유저단위)

# 오늘의 식단 API
class TodayTableAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TodayTableSerializer

    def get_queryset(self):
        try:
            queryset = TodayTable.objects.filter(
                date=date.today()
                # date__month=date.today().month,
                # date__day=date.today().day
            )
            return queryset
        except ObjectDoesNotExist:
            return ""


# 한상 식단 API
class TableListAPI(generics.ListAPIView):
    serializer_class = TableSerializer
    queryset = Table.objects.all()
    permission_classes = (IsAuthenticated,)


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
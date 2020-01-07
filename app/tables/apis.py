import calendar
from datetime import date
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *

User = get_user_model()


# 레시피 HTML rendering View
# class RecipeEditorAPIView(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'editor.html'
#
#     def get(self, request, pk):
#         table = Table.objects.get(pk=pk)
#         return Response({"table_code": table.recipe})


# 한상 식단 리스트 View
class TableListAPI(generics.ListAPIView):
    serializer_class = TableSerializer
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


# 이번 달 식단 리스트 View
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


# 식단 검색 View
class TableSearchAPI(generics.ListAPIView):
    serializer_class = TableSerializer
    permission_classes = (IsAuthenticated,)

    # Need Additional Parameter
    def get_queryset(self):
        if self.request.GET.get('keywords'):
            keywords = self.request.GET.get('keywords')
            queryset = Table.objects.filter(dietary_composition__icontains=keywords)
            return queryset
        else:
            return ""


# 메인페이지 View(Calendar + Table Log for User)
class MainPageAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # Calendar
        cal = calendar.monthrange(date.today().year, date.today().month)
        # Table Log
        user_monthly_log = TableLog.objects.filter(
            user=request.user,
            date__range=[date.today().replace(day=1), date.today().replace(day=cal[1])]
        )
        serializers = TableLogSerializer(user_monthly_log, many=True)
        log_data = {
            "calendar": cal,
            "userLog": serializers.data
        }
        return Response(log_data, status=status.HTTP_200_OK)


# Add New Table Log View
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

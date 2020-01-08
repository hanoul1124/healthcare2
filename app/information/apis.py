from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from watson import search as watson
from .serializers import *


class FNISearchView(APIView):

    # Specify default ordering
    ordering = ('id',)

    def get(self, request):
        # watson package를 사용한 full text search
        search_results = watson.search(request.GET.get['search'], models=(FNI,))
        # 검색된 object들의 pk list가 output
        index_list = [index.object_id for index in search_results]

        # FNI에서 해당 index에 해당하는 데이터 검색 후 Serializer로 복수 처리
        queryset = [FNI.objects.get(pk=f'{pk}') for pk in index_list]
        serializer = FNISerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HFASearchView(APIView):

    # Specify default ordering
    ordering = ('id',)

    def get(self, request):
        # watson package를 사용한 full text search
        search_results = watson.search(request.GET.get['search'], models=(HFA,))
        # 검색된 object들의 pk list가 output
        index_list = [index.object_id for index in search_results]

        # HFA에서 해당 index에 해당하는 데이터 검색 후 Serializer로 복수 처리
        queryset = [HFA.objects.get(pk=f'{pk}') for pk in index_list]
        serializer = HFASerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HFCSearchView(APIView):

    # Specify default ordering
    ordering = ('id',)

    def get(self, request):
        # watson package를 사용한 full text search
        search_results = watson.search(request.GET.get['search'], models=(HFC,))
        # 검색된 object들의 pk list가 output
        index_list = [index.object_id for index in search_results]

        # HFC에서 해당 index에 해당하는 데이터 검색 후 Serializer로 복수 처리
        queryset = [HFC.objects.get(pk=f'{pk}') for pk in index_list]
        serializer = HFCSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HFISearchView(APIView):

    # Specify default ordering
    ordering = ('id',)

    def get(self, request):
        # watson package를 사용한 full text search
        search_results = watson.search(request.GET.get['search'], models=(HFI,))
        # 검색된 object들의 pk list가 output
        index_list = [index.object_id for index in search_results]

        # HFI에서 해당 index에 해당하는 데이터 검색 후 Serializer로 복수 처리
        queryset = [HFI.objects.get(pk=f'{pk}') for pk in index_list]
        serializer = HFISerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
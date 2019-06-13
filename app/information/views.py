# Create your views here.

from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_RANGE,
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    LOOKUP_QUERY_EXCLUDE,
)

from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend,
    # MultiMatchSearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from . import documents
from . import serializers


class FNIViewSet(DocumentViewSet):
    document = documents.FNIDocument
    serializer_class = serializers.FNIDocumentSerializer
    lookup_field = 'pk'
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
        # MultiMatchSearchFilterBackend,
    ]

    # Define search fields
    search_fields = (
        'food_name',
        'food_group',
    )

    # Multi Match search fields(by MultiMatchSearchFilter Backend)
    # ** Not work properly
    # multi_match_search_fields = {
        # 'food_name': {'boost': 5},
        # 'food_group': {'boost': 2},
    # }

    # Filter fields
    filter_fields = {
        'id': {
            'field': 'id',
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
        # 'food_name': 'food_name.raw',
        # 'food_group': 'food_group.raw',
        'food_name': 'food_name',
        'food_group': 'food_group',
    }

    # Define ordering fields
    ordering_fields = {
        'id': 'id',
        'food_name': 'food_name.raw',
        'food_group': 'food_group.raw',
    }

    # Specify default ordering
    ordering = ('id',)


# HFI Search View
class HFIViewSet(DocumentViewSet):
    document = documents.HFIDocument
    serializer_class = serializers.HFIDocumentSerializer
    lookup_field = 'pk'
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]

    # Define Search Fields
    search_fields = (
        'material_name',
        'feature',
        'caution'
    )

    filter_fields = {
        'material_name': 'material_name.raw',
        'feature': 'feature',
        'caution': 'caution',
    }

    # Define Ordering Fields
    ordering_fields = {
        'id': 'id',
        'material_name': 'material_name.raw',
    }

    # Specify Default Ordering
    ordering = ('id',)


# HFC Search View
class HFCViewSet(DocumentViewSet):
    document = documents.HFCDocument
    serializer_class = serializers.HFCDocumentSerializer
    lookup_field = 'pk'
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]

    # Define Search Fields
    search_fields = (
        'material_name',
        'ingredient',
        'feature',
        'caution'
    )

    filter_fields = {
        'material_name': 'material_name.raw',
        'ingredient': 'ingredient.raw',
        'feature': 'feature',
        'caution': 'caution',
    }

    # Define Ordering Fields
    ordering_fields = {
        'id': 'id',
        'ingredient': 'ingredient.raw',
    }

    # Specify Default Ordering
    ordering = ('id',)


# HFC Search View
class HFAViewSet(DocumentViewSet):
    document = documents.HFADocument
    serializer_class = serializers.HFADocumentSerializer
    lookup_field = 'pk'
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]

    # Define Search Fields
    search_fields = (
        'material_name',
        'company',
        'feature',
        'caution'
    )

    filter_fields = {
        'material_name': 'material_name.raw',
        'company': 'company',
        'feature': 'feature',
        'caution': 'caution',
    }

    # Define Ordering Fields
    ordering_fields = {
        'id': 'id',
        'material_name': 'material_name.raw',
    }

    # Specify Default Ordering
    ordering = ('id',)
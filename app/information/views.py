# Create your views here.

from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_RANGE, LOOKUP_QUERY_IN, LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE, LOOKUP_QUERY_LT, LOOKUP_QUERY_LTE
)

from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend
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
    ]

    # Define search fields
    search_fields = (
        'food_name',
        'food_group',
    )

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
        'food_name': 'food_name.raw',
        'food_group': 'food_group.raw',
    }

    # Define ordering fields
    ordering_fields = {
        'id': 'id',
        'food_name': 'food_name.raw',
        'food_group': 'food_group.raw',
    }

    # Specify default ordering
    ordering = ('id',)
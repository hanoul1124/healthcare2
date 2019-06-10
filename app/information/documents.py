from django_elasticsearch_dsl import Index, DocType, fields
from elasticsearch_dsl import connections
from .models import *

# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost:9200'])

# Name of the Elasticsearch index
fni_index = Index('fnis')

# See Elasticsearch Indices API reference for available settings
fni_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@fni_index.doc_type
class FNIDocument(DocType):
    class Meta:
        # The model associated with this DocType
        model = FNI
        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'food_name',
            'food_group',
            'food_amount',
            'calorie',
            'carbs',
            'protein',
            'fat',
            'sugar',
            'salt',
            'cholesterol',
            'saturated_fatty_acid',
            'trans_fat'
        ]

    id = fields.IntegerField(attr='pk')


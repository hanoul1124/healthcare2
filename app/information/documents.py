from django_elasticsearch_dsl import Index, DocType, fields
from elasticsearch_dsl import connections, analyzer
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

nori_analyzer = analyzer(
    'nori_analyzer',
    tokenizer="nori_tokenizer"
)

@fni_index.doc_type
class FNIDocument(DocType):
    id = fields.IntegerField(attr='pk')
    food_name = fields.StringField(
        # analyzer 로 사용할 것 지정
        analyzer=nori_analyzer,
        # field_name.raw = analyzer를 keyword(built-in analyzer)로 사용한
        # 결과를 돌려준다.
        fields={
            'raw': fields.StringField(analyzer='keyword'),
        }
    )
    food_group = fields.StringField(
        analyzer=nori_analyzer,
        fields={
            'raw': fields.StringField(analyzer='keyword'),
        }
    )
    food_amount = fields.StringField()
    calorie = fields.StringField()
    carbs = fields.StringField()
    protein = fields.StringField()
    fat = fields.StringField()
    sugar= fields.StringField()
    salt= fields.StringField()
    cholesterol = fields.StringField()
    saturated_fatty_acid = fields.StringField()
    trans_fat = fields.StringField()

    class Meta:
        # The model associated with this DocType
        model = FNI
        # The fields of the model you want to be indexed in Elasticsearch
    #     fields = [
    #         'food_name',
    #         'food_group',
    #         'food_amount',
    #         'calorie',
    #         'carbs',
    #         'protein',
    #         'fat',
    #         'sugar',
    #         'salt',
    #         'cholesterol',
    #         'saturated_fatty_acid',
    #         'trans_fat'
    #     ]
    #
    # id = fields.IntegerField(attr='pk')


# from django_elasticsearch_dsl import Index, DocType, fields
# from elasticsearch_dsl import connections, analyzer
# from .models import *
#
# # Define a default Elasticsearch client
# connections.create_connection(hosts=['localhost:9200'])
#
# # Name of the Elasticsearch index
# fni_index = Index('fnis')
# hfi_index = Index('hfis')
# hfc_index = Index('hfcs')
# hfa_index = Index('hfas')
#
# # See Elasticsearch Indices API reference for available settings
# fni_index.settings(
#     number_of_shards=1,
#     number_of_replicas=0
# )
# hfi_index.settings(
#     number_of_shards=1,
#     number_of_replicas=0
# )
# hfc_index.settings(
#     number_of_shards=1,
#     number_of_replicas=0
# )
# hfa_index.settings(
#     number_of_shards=1,
#     number_of_replicas=0
# )
#
#
# # Nori 형태소 분석기 사용(ElasticSearch 공식 한글 형태소 분석 플러그인)
# nori_analyzer = analyzer(
#     'nori_analyzer',
#     tokenizer="nori_tokenizer"
# )
#
#
# # Index 정의
# @fni_index.doc_type
# class FNIDocument(DocType):
#     id = fields.IntegerField(attr='pk')
#     food_name = fields.StringField(
#         # analyzer 로 사용할 것 지정
#         analyzer=nori_analyzer,
#         # field_name.raw = analyzer를 keyword(built-in analyzer)로 사용한
#         # 결과를 돌려준다.
#         fields={
#             'raw': fields.StringField(analyzer='keyword'),
#         }
#     )
#     food_group = fields.StringField(
#         analyzer=nori_analyzer,
#         fields={
#             'raw': fields.StringField(analyzer='keyword'),
#         }
#     )
#     food_amount = fields.StringField()
#     calorie = fields.StringField()
#     carbs = fields.StringField()
#     protein = fields.StringField()
#     fat = fields.StringField()
#     sugar= fields.StringField()
#     salt= fields.StringField()
#     cholesterol = fields.StringField()
#     saturated_fatty_acid = fields.StringField()
#     trans_fat = fields.StringField()
#
#     class Meta:
#         # The model associated with this DocType
#         model = FNI
#         # The fields of the model you want to be indexed in Elasticsearch
#     #     fields = [
#     #         'food_name',
#     #         'food_group',
#     #         'food_amount',
#     #         'calorie',
#     #         'carbs',
#     #         'protein',
#     #         'fat',
#     #         'sugar',
#     #         'salt',
#     #         'cholesterol',
#     #         'saturated_fatty_acid',
#     #         'trans_fat'
#     #     ]
#     #
#     # id = fields.IntegerField(attr='pk')
#
#
# @hfi_index.doc_type
# class HFIDocument(DocType):
#     id = fields.IntegerField(attr='pk')
#     material_name = fields.StringField(
#         analyzer=nori_analyzer,
#         fields={
#             'raw': fields.StringField(analyzer='keyword'),
#         }
#     )
#     material_number = fields.StringField(
#         analyzer=nori_analyzer,
#         fields={
#             'raw': fields.StringField(analyzer='keyword'),
#         }
#     )
#     daily_limit = fields.StringField()
#     feature = fields.TextField(analyzer=nori_analyzer)
#     caution = fields.TextField(analyzer=nori_analyzer)
#
#     class Meta:
#         model = HFI
#
#
# @hfc_index.doc_type
# class HFCDocument(DocType):
#     id = fields.IntegerField(attr='pk')
#     material_name = fields.StringField(
#         analyzer=nori_analyzer,
#         fields={
#             'raw': fields.StringField(analyzer='keyword'),
#         }
#     )
#     ingredient = fields.StringField(
#         analyzer=nori_analyzer,
#         fields={
#             'raw': fields.StringField(analyzer='keyword'),
#         }
#     )
#     daily_limit = fields.StringField(attr='daily_limit')
#     feature = fields.TextField(
#         attr='modified_feature',
#         analyzer=nori_analyzer
#     )
#     caution = fields.TextField(analyzer=nori_analyzer)
#
#     class Meta:
#         model = HFC
#
#
# @hfa_index.doc_type
# class HFADocument(DocType):
#     id = fields.IntegerField(attr='pk')
#     material_name = fields.StringField(
#         analyzer=nori_analyzer,
#         fields={
#             'raw': fields.StringField(analyzer='keyword'),
#         }
#     )
#     company = fields.StringField(
#         analyzer=nori_analyzer,
#     )
#     daily_intake = fields.StringField()
#     feature = fields.TextField(analyzer=nori_analyzer)
#     caution = fields.TextField(
#         attr='modified_caution',
#         analyzer=nori_analyzer
#     )
#
#     class Meta:
#         model = HFA

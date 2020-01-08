from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import *


class NutrientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrient
        fields = (
            'calorie',
            'carbs',
            'fiber',
            'A_protein',
            'V_protein',
            'A_fat',
            'V_fat',
            'cholesterol',
            'salt',
            'potassium',
            'phosphorus',
            'A_calcium',
            'V_calcium',
            'V_iron',
            'A_iron'
        )


class TableSerializer(serializers.ModelSerializer):
    nutrient = NutrientSerializer()
    # recipe_url = serializers.SerializerMethodField()

    class Meta:
        model = Table
        fields = (
            'pk',
            'date',
            'time',
            'dietary_composition',
            'ingredients',
            'recipe',
            'tips',
            'nutrient'
        )


class TableCompactSerializer(serializers.ModelSerializer):
    nutrient = NutrientSerializer()

    class Meta:
        model = Table
        fields = (
            'pk',
            'dietary_composition',
            'nutrient'
        )


class TableLogSerializer(serializers.ModelSerializer):
    table = TableCompactSerializer()

    class Meta:
        model = TableLog
        fields = (
            'user',
            'table',
            'date',
            'time'
        )


class MakeTableLogSerializer(serializers.Serializer):
    table_pk = serializers.IntegerField()
    meal_time = serializers.CharField()

    def validate(self, attrs):
        table_pk = attrs.get('table_pk')
        meal_time = attrs.get('meal_time')
        available_meal_time = ['아침', '점심', '저녁', '간식']
        try:
            if Table.objects.get(pk=table_pk) and meal_time in available_meal_time:
                return attrs
        except ObjectDoesNotExist:
            raise serializers.ValidationError("해당 식단이 존재하지 않거나 식사 시간 설정이 잘못되었습니다.")

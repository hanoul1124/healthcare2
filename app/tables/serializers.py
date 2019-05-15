from rest_framework import serializers
from .models import Table
from .models import Nutrient


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
        )


class TableSerializer(serializers.ModelSerializer):
    nutrients = NutrientSerializer()

    class Meta:
        model = Table
        fields = (
            'dietary_composition',
            'recipe',
            'nutrients'
        )
from .models import *
from rest_framework import serializers


class FNISerializer(serializers.ModelSerializer):
    class Meta:
        model = FNI
        fields = (
            'id',
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
        )


class HFISerializer(serializers.ModelSerializer):
    class Meta:
        model = HFI
        fields = (
            'id',
            'material_name',
            'material_number',
            'daily_limit',
            'feature',
            'caution'
        )


class HFCSerializer(serializers.ModelSerializer):
    class Meta:
        model = HFC
        fields = (
            'id',
            'material_name',
            'ingredient',
            'daily_limit',
            'feature',
            'caution'
        )


class HFASerializer(serializers.ModelSerializer):
    class Meta:
        model = HFA
        fields = (
            'id',
            'material_name',
            'company',
            'daily_intake',
            'feature',
            'caution'
        )
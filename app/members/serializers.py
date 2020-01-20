import re
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'name',
            'email',
            'phone_number',
            'gender',
            'height',
            'weight',
            'renal_disease',
            'hospital',
            'attending_physician',
        )


class CheckUniqueIDSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate(self, data):
        try:
            if User.objects.get(username=data['username']):
                raise ValidationError("username already exists")
        except (AttributeError, ObjectDoesNotExist):
            return data


class PhoneNumberVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate(self, data):
        phone = data['phone_number']
        if not re.match('^01\d{8,9}$', phone):
            raise ValidationError("0-9로 이루어진 10-11자리 숫자를 입력하세요.")
        return data


class SocialAuthTokenSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    name = serializers.CharField(allow_blank=True, allow_null=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        
    def validate(self, data):
        # 이미 있는 유저라면 user id를 매치하여 리턴
        # 없다면 새롭게 생성
        username = data['user_id']
        user = authenticate(username=username)
        if not user:
            user = User.objects.create_user(
                username=self.user_id,
                name=self.name,
                phone_verification=True,
            )
        self.user = user
        return data
        
    


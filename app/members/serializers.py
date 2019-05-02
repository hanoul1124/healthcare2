import re
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from members.models import Profile
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
        )


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            # 'user',
            'gender',
            'height',
            'weight',
            'renal_disease',
            # 'email',
            'hospital',
            'attending_physician',
        )
        # read_only_fields = ('user',)


class UserInfoSerializer(serializers.ModelSerializer):
    # profile = serializers.SerializerMethodField()
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'name',
            'email',
            'phone_number',
            'profile',
        )
        read_only_fields = ('username',)

    # def get_profile(self, user):
    #     profile_serializer = ProfileSerializer(user.profile)
    #     return profile_serializer.data

    # Nested writable serializer(ex profile = ProfileSerializer() > serializer.save())
    # 이를 사용하기 위해서는, Serializer에 .create(), .update()를 explicit하게 작성하거나,
    # ProfileSerializer(read_only=True)를 사용해야만 한다.
    def create(self, validated_data):
        # 일단 프로필을 먼저 빼둔다
        profile = validated_data.pop('profile')
        # 프로필을 뺐기 때문에 user 객체 정보만 남는다
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, **profile)
        return user

    def update(self, user, validated_data):
        profile_data = validated_data.pop('profile')
        profile_instance = user.profile
        profile_instance.gender = profile_data.get('gender')
        profile_instance.height = profile_data.get('height')
        profile_instance.weight = profile_data.get('weight')
        profile_instance.renal_disease = profile_data.get('renal_disease')
        profile_instance.attending_physician = profile_data.get('attending_physician')
        profile_instance.save()

        user.set_password(validated_data.get('password'))
        user.name = validated_data.get('name')
        user.phone_number = validated_data.get('phone_number')
        user.email = validated_data.get('email')
        user.save()

        return user

class CheckUniqueIDSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate(self, data):
        if User.objects.get(username=data['username']):
            raise ValidationError("username already exists")
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
        
    


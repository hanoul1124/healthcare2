# TODO :
#  ElasticSearch : 검색기능 구현(DB)
#  DRF Swagger(ysag) : API 문서화 작업용
#  Celery(+Redis, + Naver SENS) : 문자인증을 위한 Naver SENS API 비동기 작동
#  POSTMAN 설치 후 사용(DRF API Check)
import json
import os
import random

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
import requests

from .serializers import UserSerializer, PhoneNumberVerificationSerializer, CheckUniqueIDSerializer, \
    SocialAuthTokenSerializer, UserInfoSerializer

User = get_user_model()

class SignupView(generics.CreateAPIView):
    '''
    회원가입 API.
    아래 4개 항목을 입력해 전달하면, 타입 유효성 검사 후 가입 처리
        'username',
        'password',
        'name',
        'phone_number'"user
    이외의 데이터는 추가 정보 기입(마이페이지)에 생성.
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


class CheckUniqueIDView(APIView):
    '''
    유저 ID 중복검사를 위한 View
    validation 과정에서 입력한 ID가 이미 존재하는지 체크
    "unique_id" : True / False 를 리턴한다.
    '''
    def post(self, request):
        serializer = CheckUniqueIDSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                "unique_id": True,
                "message": "사용 가능한 아이디입니다."
            }, status=status.HTTP_200_OK)
        return Response({
            "unique_id": False,
            "message": "이미 존재하는 아이디입니다."
        }, status=status.HTTP_200_OK)


root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
secrets = json.load(open(os.path.join(os.path.join(root_dir, '.secrets'), 'base.json')))


class PhoneNumberVerificationView(APIView):
    '''
    휴대폰 번호 인증을 위한 NAVER SENS API 연동
    휴대폰 번호를 전달하면 정규식 검증(10-11자리 숫자로 이루어진 문자열 여부 확인, - 제외)
    유효한 형식임이 확인되면 NAVER SENS를 통해 입력된 번호로 랜덤 인증번호(1000~9999 사이) 발송
    발송에 성공한 경우 {"verifiation" : <인증번호> , "message" : <인증 성공>} 전달
    실패했을 경우 {"verification" : False, "message" : <인증 실패> 전달
    '''
    # throttle classes : 익명 유저의 verification 신청 횟수 제한
    throttle_classes = (AnonRateThrottle,)

    def post(self, request):
        serializer = PhoneNumberVerificationSerializer(data=request.data)
        if serializer.is_valid():
            service_id = secrets['SENS_SERVICE_ID']
            random_num = str(random.randrange(1000, 9999))
            send_url = f'https://api-sens.ncloud.com/v1/sms/services/{service_id}/messages'
            headers = {
                "Content-Type": "application/json; charset=utf-8",
                "X-NCP-auth-key": "Ewp30enbXCGCzuLlOz7o",
                "X-NCP-service-secret": "566ef845c0514626b337427cab165cc8"
            }
            body = {
                "type": "SMS",
                "from": secrets['FROM_PHONE_NUMBER'],
                "to": [
                    serializer.data['phone_number']
                ],
                "content": "인증번호는 " + random_num + "입니다."
            }
            res = requests.post(send_url, headers=headers, data=json.dumps(body))
            if not res.json()['status'] == '200':
                return Response({"verification": False, "verificationNumber": "", "message": "인증번호 발송에 실패했습니다."},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response({"verification": True, "verificationNumber": random_num, "message": "인증번호가 발송되었습니다."},
                            status=status.HTTP_202_ACCEPTED)


class AuthTokenView(APIView):
    '''
    Login View.
    Post 요청으로 username, password를 받아
    serializer에서 사용자인증(authenticate)에 성공하면
    해당 사용자와 연결된 토큰 정보를 리턴하거나 없다면 새로 생성한다.
    '''
    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SocialAuthTokenView(APIView):
    '''
    Social Login View.
    Post 요청으로 iOS-SNS API 통신으로 전달받은 user_id를 확인하여
    이미 있던 계정이면 그에 해당하는 토큰을, 없다면 새롭게 토큰을 생성한다.
    '''
    def post(self, request):
        serializer = SocialAuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.user)[0]
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    '''
    로그아웃 View. 유저에 할당되었던 토큰을 삭제해준다.
    delete method로 request를 요청해야함
    유저가 토큰을 가지고 있을 경우에만 접근 가능(IsAuthenticated)
    '''
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            return Response({"logout": True, "message": "이미 로그아웃 처리되었습니다."},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({"logout": True}, status=status.HTTP_200_OK)


# @transaction.atomic
class UserInfoView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # token key부터 받고 key로 유저 인식시키기.
        # user_profile = get_object_or_404(Profile, user=request.user)
        serializer = UserInfoSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = UserInfoSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.update(request.user, serializer.validated_data)
        return Response({"message": "수정되었습니다."}, status=status.HTTP_200_OK)



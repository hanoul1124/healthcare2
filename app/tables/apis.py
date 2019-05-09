from django.contrib.auth import get_user_model
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()


class ExampleAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'tables/example.html'

    def get(self, request):
        queryset = User.objects.all()
        return Response({"user_list": queryset})

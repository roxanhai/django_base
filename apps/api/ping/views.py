import os

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def ping(request):
    print(os.environ.get('DB_NAME'))
    return Response('pong')
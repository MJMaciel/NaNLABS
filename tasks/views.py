from rest_framework.decorators import api_view
from rest_framework.response import Response

from .functions import card_factory
from .serializers import TaskSerializer


@api_view(['POST'])
def task_creator(request):
    serializer = TaskSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    card_response = card_factory(serializer.data)
    return Response(card_response)
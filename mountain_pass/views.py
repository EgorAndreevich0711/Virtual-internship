from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import MountainPassSerializer
from .database import DatabaseManager

class SubmitDataView(APIView):
    def post(self, request):
        serializer = MountainPassSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Используем наш DatabaseManager для создания перевала
                mountain_pass = DatabaseManager.create_mountain_pass(request.data)
                return Response(
                    {'status': status.HTTP_200_OK, 'message': 'Отправлено успешно', 'id': mountain_pass.id},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

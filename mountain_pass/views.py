from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MountainPass
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

class UpdatePassStatusView(APIView):
    def patch(self, request, pass_id):
        new_status = request.data.get('status')
        try:
            updated_pass = DatabaseManager.update_status(pass_id, new_status)
            return Response({"new_status": updated_pass.status}, status=200)
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)

class MountainPassDetail(RetrieveAPIView):
    queryset = MountainPass.objects.all()
    serializer_class = MountainPassSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class MountainPassUpdate(UpdateAPIView):
    queryset = MountainPass.objects.all()
    serializer_class = MountainPassSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != 'new':
            return Response(
                {"state": 0, "message": "Редактирование запрещено: статус не 'new'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        protected_fields = ['email', 'phone', 'fam', 'name', 'otc']
        for field in protected_fields:
            if field in request.data.get('user', {}):
                return Response(
                    {"state": 0, "message": f"Запрещено изменять поле: {field}"},
                    status=status.HTTP_403_FORBIDDEN
                )

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"state": 1, "message": "Успешно обновлено"})
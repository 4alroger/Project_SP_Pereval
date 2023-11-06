import django_filters
from rest_framework.response import Response

from .serializers import *
from rest_framework import viewsets, status, generics
from django.http import JsonResponse


class CoordsViewSet(viewsets.ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer


class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class MountViewSet(viewsets.ModelViewSet):
    queryset = Mount.objects.all()
    serializer_class = MountSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["user__email"]


    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


    def create(self, request, *args, **kwargs):
        serializer = MountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_200_OK,
                'message': None,
                'id': serializer.data['id'],
            })
        if status.HTTP_400_BAD_REQUEST:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Bad Request',
                'id': None,
            })
        if status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Ошибка подключения к базе данных',
                'id': None,
            })

    # редактирование данных перевала, при статусе "new" без изменений данных пользователя
    def partial_update(self, request, *args, **kwargs):
        record = self.get_object()
        if record.status == 'new':
            serializer = MountSerializer(record, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'state': '1',
                        'message': 'Изменения внесены успешно'
                    }
                )
            else:
                return Response(
                    {
                        'state': '0',
                        'message': serializer.errors
                    }
                )
        else:
            return Response(
                {
                    'state': '0',
                    'message': f'При данном статусе: {record.get_status_display()}, данные изменить нельзя!'
                }
            )

"""Класс работы с БД для второго спринта: извлечение и редактирование перевала"""
class MountDetailViewSet(viewsets.ModelViewSet):
    queryset = Mount.objects.all()
    serializer_class = MountDetailSerializer

    def update(self, request, *args, **kwargs):
        """
        Переопределение метода update(PATCH)
        """
        pk = kwargs.get("pk", None)

        try:
            instance = Mount.objects.get(pk=pk)
        except:
            return Response({"error": "Такого перевала не существует"}, status=400)

        if instance.status != "N":
            return Response({"message": "Перевал на модерации, вы не можете его изменить",
                             "state": 0}, status=400)
        else:
            serializer = MountDetailSerializer(data=request.data, instance=instance)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"state": 1}, status=200)


""" Список данных обо всех перевалах, которые пользователь с почтой <email> отправил на сервер """
class EmailAPIView(generics.ListAPIView):
    serializer_class = AuthEmailMountSerializer
    def get(self, request, *args, **kwargs):
        email = kwargs.get('email', None)
        if Mount.objects.filter(user__email=email):
            data = AuthEmailMountSerializer(Mount.objects.filter(user__email=email), many=True).data
            api_status = status.HTTP_200_OK
        else:
            data = {
                'message': f'Не существует пользователя с таким email - {email}'
            }
            api_status = 404
        return JsonResponse(data, status=api_status, safe=False)
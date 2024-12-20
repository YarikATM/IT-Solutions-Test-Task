from django.shortcuts import render
from rest_framework import generics
from API.models import Car, Comment
from API.permissions import MyIsAuthenticatedOrReadOnly
from rest_framework import filters
from API.serializers import (
    CarSerializer,
    CommentSerializer
)
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiTypes
)



@extend_schema_view(
    get=extend_schema(tags=["Cars"], summary="Получение списка Cars",
                      parameters=[OpenApiParameter('search', OpenApiTypes.STR, description='Поиск')]),
    post=extend_schema(tags=["Cars"], summary="Создание нового обьекта Car"),
)

class CarListCreateView(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [MyIsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['make', 'model', 'year']


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@extend_schema_view(
    delete=extend_schema(tags=["Cars"], summary="Удаление обьекта Car",),
    get=extend_schema(tags=["Cars"], summary="Получение конкретного обьекта Car"),
    put=extend_schema(tags=["Cars"], summary="Полное обновление обьекта Car"),
    patch=extend_schema(tags=["Cars"], summary="Частичное обновление обьекта Car"),
)
class CarRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [MyIsAuthenticatedOrReadOnly]

@extend_schema_view(
    get=extend_schema(tags=["Comments"], summary="Получение конкретного обьекта Comment"),
    post=extend_schema(tags=["Comments"], summary="Создание нового обьекта Comment"),
)
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [MyIsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(car=self.kwargs.get('pk'))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, car_id=self.kwargs.get('pk'))


from django.urls import path, include
from web.views import (CarListView, CarCreateView,
                       CarDetailView, CarUpdateView,
                       CarDeleteView, CommentCreateView)

urlpatterns = [
    path("", CarListView.as_view(), name='web_car_list'),
    path("cars/new/", CarCreateView.as_view(), name='web_car_new'),
    path("cars/<int:pk>", CarDetailView.as_view(), name='web_car_detail'),
    path("cars/<int:pk>/edit/", CarUpdateView.as_view(), name='web_car_edit'),
    path("cars/<int:pk>/delete/", CarDeleteView.as_view(), name='web_car_delete'),


    path("cars/<int:pk>/comments/create", CommentCreateView.as_view(), name="web_comments_create"),
]


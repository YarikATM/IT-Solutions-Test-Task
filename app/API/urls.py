from django.urls import path
from API.views import CarListCreateView, CarRetrieveUpdateDestroyView, CommentListCreateView

urlpatterns = [
    path('', CarListCreateView.as_view(), name='car_list'),
    path('<int:pk>/', CarRetrieveUpdateDestroyView.as_view(), name='car_detail'),
    path('<int:pk>/comment', CommentListCreateView.as_view(), name='comment_list')
]
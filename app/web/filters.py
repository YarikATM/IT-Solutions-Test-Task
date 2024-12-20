import django_filters
from API.models import Car
from django.db.models import Q
from django import forms


class CarFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='my_custom_filter', label='Search')


    class Meta:
        model = Car
        fields = ['q']


    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(make__icontains=value) |
            Q(model__icontains=value)
        )

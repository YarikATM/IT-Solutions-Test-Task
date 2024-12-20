from django.db import models
from django.contrib.auth import get_user_model
User=get_user_model()
from django.shortcuts import reverse





class Car(models.Model):
    make = models.CharField(max_length=100, verbose_name='Марка')
    model = models.CharField(max_length=100, verbose_name='Модель')
    year = models.PositiveIntegerField(verbose_name='Год выпуска')
    description = models.TextField(verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

    def get_absolute_url(self):
        return reverse("web_car_detail", kwargs={"pk": self.pk})


    class Meta:
        ordering = ['-created_at']




class Comment(models.Model):
    content = models.TextField(verbose_name='Содержимое комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    car = models.ForeignKey(Car, related_name='comments', on_delete=models.CASCADE, verbose_name='Автомобиль')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')

    def __str__(self):
        return f"Comment by {self.user.username} on {self.car.make} {self.car.model}"

    class Meta:
        ordering = ['-created_at']

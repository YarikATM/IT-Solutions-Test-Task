from http.client import responses

from rest_framework.test import APITestCase
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
User=get_user_model()
from API.models import Car, Comment
from API.serializers import CarSerializer, CommentSerializer



class CarListCreateViewTest(APITestCase):
    fixtures = ['users.json', 'cars.json']


    def test_list_car(self):
        response = self.client.get(reverse('car_list'))
        expected_data = CarSerializer(Car.objects.all(), many=True).data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)


    def test_create_car(self):
        user = User.objects.first()
        self.client.force_login(user)
        data = {
            'make': 'Toyota',
            'model': 'Camry',
            'year': 2020,
            'description': 'New car',
        }
        response = self.client.post(reverse('car_list'), data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Car.objects.count(), 4)



class CarRetrieveUpdateDestroyViewTest(APITestCase):
    fixtures = ['users.json', 'cars.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.car = Car.objects.get(pk=1)
        self.another_user = User.objects.get(pk=2)

    def test_get_car_detail(self):
        response = self.client.get(reverse('car_detail', kwargs={"pk": self.car.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, CarSerializer(self.car).data)


    def test_delete_car_detail_without_user(self):
        response = self.client.delete(reverse('car_detail', kwargs={"pk": self.car.pk}))
        self.assertEqual(response.status_code, 403)

    def test_delete_car_detail_with_another_user(self):
        self.client.force_login(self.another_user)
        response = self.client.delete(reverse('car_detail', kwargs={"pk": self.car.pk}))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Car.objects.filter(pk=self.car.pk).count(), 1)

    def test_delete_car_detail_with_right_user(self):
        self.client.force_login(self.user)
        response = self.client.delete(reverse('car_detail', kwargs={"pk": self.car.pk}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Car.objects.filter(pk=self.car.pk).count(), 0)


    def test_update_car_detail_without_user(self):
        response = self.client.put(reverse('car_detail', kwargs={"pk": self.car.pk}), {'make': 'Updated Toyota'})
        self.assertEqual(response.status_code, 403)
        response = self.client.patch(reverse('car_detail', kwargs={"pk": self.car.pk}), {'make': 'Updated Toyota'})
        self.assertEqual(response.status_code, 403)

    def test_update_car_detail_another_user(self):
        self.client.force_login(self.another_user)
        response = self.client.put(reverse('car_detail', kwargs={"pk": self.car.pk}), {'make': 'Updated Toyota'})
        self.assertEqual(response.status_code, 403)
        response = self.client.patch(reverse('car_detail', kwargs={"pk": self.car.pk}), {'make': 'Updated Toyota'})
        self.assertEqual(response.status_code, 403)


    def test_update_car_detail_user(self):
        self.client.force_login(self.user)
        response = self.client.put(reverse('car_detail', kwargs={"pk": self.car.pk}),
                                   {
                                    'make': 'Updated Toyota',
                                    'model': 'Updated Camry',
                                    'year': 2021,
                                    'description': 'Updated car'
                                   })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('make'), 'Updated Toyota')

        response = self.client.patch(reverse('car_detail', kwargs={"pk": self.car.pk}), {'make': 'Updated Toyota2'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('make'), 'Updated Toyota2')


class CommentListCreateViewTest(APITestCase):
    fixtures = ['users.json', 'cars.json', 'comments.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.car = Car.objects.get(pk=1)


    def test_create_comment_without_user(self):
        response = self.client.post(reverse('comment_list', kwargs={"pk": self.car.pk}), {'content': 'New comment'})
        self.assertEqual(response.status_code, 403)

    def test_create_comment_with_user(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('comment_list', kwargs={"pk": self.car.pk}), {'content': 'New comment'})
        self.assertEqual(response.status_code, 201)
        comment = Comment.objects.first()
        self.assertEqual(response.data, CommentSerializer(comment).data)

    def test_get_detail_comment(self):
        comment = Comment.objects.last()
        response = self.client.get(reverse('comment_list', kwargs={"pk": comment.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0], CommentSerializer(comment).data)
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .serializers import MountSerializer
from .models import *
from django.urls import reverse
from .views import EmailAPIView
import json
from datetime import datetime
from django.utils import timezone

class MountTestCase(APITestCase):
    def setUp(self):
        self.pass_4 = Mount.objects.create(
            user=User.objects.create(
                email="test1@mail.ru",
                fam="Test1",
                name="Test1",
                otc="Test1",
                phone="111"
            ),
            beauty_title="Test1",
            title="Test1",
            other_titles="Test1",
            connect='',
            coords=Coords.objects.create(
                latitude=1,
                longitude=1,
                height=1
            ),
            level=Level.objects.create(
                winter='1b',
                summer='',
                autumn='',
                spring=''
            ),
        )
        self.photo_4 = Photo.objects.create(
            data="https://pereval.online/imagecache/original/caubasephotos2.narod.ru--photos2--cau_11875_ot.jpg",
            title="Test1",
            pereval=self.pass_4
            )

        self.pass_5 = Mount.objects.create(
                user=User.objects.create(
                email="test2@mail.ru",
                fam="Test2",
                name="Test2",
                otc="Test2",
                phone="222"
            ),
            beauty_title="Test2",
            title="Test2",
            other_titles="Test2",
            connect='',
            coords=Coords.objects.create(
                latitude=2,
                longitude=2,
                height=2
            ),
            level=Level.objects.create(
                winter='2b',
                summer='',
                autumn='',
                spring=''
            ),
        )
        self.photo_5=Photo.objects.create(
            data="https://pereval.online/imagecache/original/caubasephotos1.narod.ru--photos--cau_1849_as.jpg",
            title="Test2",
            pereval=self.pass_5
            )

    def test_get_list(self):
        url = reverse('pass')
        response = self.client.get(url)
        serializer_data = MountSerializer([self.pass_4, self.pass_5], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(len(serializer_data), 2)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.json())
    def test_get_detail(self):
        url = reverse('pass-detail', args=(self.pass_4.id,))
        response = self.client.get(url)
        serializer_data = MountSerializer(self.pass_4).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.json())

    def test_get_by_email(self):
        url = reverse('email-pass', args=(self.pass_4.user.email,))
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)


class MountSerializerTestCase(TestCase):
     def setUp(self):
         self.pass_4 = Mount.objects.create(
             id=4,
             beauty_title="Test1",
             title="Test1",
             other_titles="Test1",
             connect="",
             add_time="",
             user=User.objects.create(
                 email="test1@mail.ru",
                 fam="Test1",
                 name="Test1",
                 otc="Test1",
                 phone="111"
             ),
             coords=Coords.objects.create(
                 latitude=1.0,
                 longitude=1.0,
                 height=1
             ),
             level=Level.objects.create(
                 winter="1b",
                 summer="",
                 autumn="",
                 spring=""
             ),
         )
         self.photo_4 = Photo.objects.create(
            data="https://pereval.online/imagecache/original/caubasephotos2.narod.ru--photos2--cau_11875_ot.jpg",
            title="Test1",
            pereval=self.pass_4
         )

         self.pass_2 = Mount.objects.create(
             id=5,
             beauty_title="Test2",
             title="Test2",
             other_titles="Test2",
             connect="",
             add_time="",
             user=User.objects.create(
                 email="test2@mail.ru",
                 fam="Test2",
                 name="Test2",
                 otc="Test2",
                 phone="222"
             ),
             coords=Coords.objects.create(
                 latitude=2.0,
                 longitude=2.0,
                 height=2
             ),
             level=Level.objects.create(
                 winter="2b",
                 summer="",
                 autumn="",
                 spring=""
             ),
         )
         self.photo_5 = Photo.objects.create(
            data="https://pereval.online/imagecache/original/caubasephotos1.narod.ru--photos--cau_1849_as.jpg",
            title="Test2",
            pereval=self.pass_5
         )

     def test_check(self):
         serializer_data = MountSerializer([self.pass_4, self.pass_5], many=True).data
         expected_data = [
             {
                 "id": 4,
                 "beauty_title": "Test1",
                 "title": "Test1",
                 "other_titles": "Test1",
                 "connect": "",
                 "add_time": str(self.pass_4.add_time),
                 "user": {
                    "email": "test1@mail.ru",
                    "fam": "Test1",
                    "name": "Test1",
                    "otc": "Test1",
                    "phone": "111"
                 },
                 "coords": {
                    "latitude": 1.0,
                    "longitude": 1.0,
                    "height": 1
                 },
                 "level": {
                     "winter": "1b",
                     "summer": "",
                     "autumn": "",
                     "spring": ""
                 },
                 "images": [
                     {
                        "data": "https://pereval.online/imagecache/original/caubasephotos2.narod.ru--photos2--cau_11875_ot.jpg",
                        "title": "Test1"
                     },
                 ],
                 "status": ""
             },
             {
                 "id": 5,
                 "beauty_title": "Test2",
                 "title": "Test2",
                 "other_titles": "Test2",
                 "connect": "",
                 "add_time": str(self.pass_2.add_time),
                 "user": {
                    "email": "test2@mail.ru",
                    "fam": "Test2",
                    "name": "Test2",
                    "otc": "Test2",
                    "phone": "222"
                 },
                 "coords": {
                     "latitude": 2.0,
                     "longitude": 2.0,
                     "height": 2
                 },
                 "level": {
                     "winter": "2b",
                     "summer": "",
                     "autumn": "",
                     "spring": ""
                 },
                 "images": [
                     {
                        "data": "https://pereval.online/imagecache/original/caubasephotos1.narod.ru--photos--cau_1849_as.jpg",
                        "title": "Test2"
                     },
                 ],
                 "status": ""
             }
         ]
         # print(expected_data)
         # print(serializer_data)
         self.assertEqual(expected_data,serializer_data)
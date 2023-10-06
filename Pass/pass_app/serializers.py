from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone', 'last_name', 'name', 'otc', ]

    def save(self, **kwargs):
        self.is_valid()
        user = User.objects.filter(email=self.validated_data.get('email'))
        if user.exists():
            return user.first()
        else:
            new_user = User.objects.create(
                email=self.validated_data.get('email'),
                phone=self.validated_data.get('phone'),
                fam=self.validated_data.get('last_name'),
                name=self.validated_data.get('name'),
                otc=self.validated_data.get('otc'),
            )
        return new_user


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['winter', 'summer', 'autumn', 'spring']


class PhotoSerializer(serializers.ModelSerializer):
    data = serializers.URLField()

    class Meta:
        model = Photo
        fields = ['data', 'title']


class MountSerializer(WritableNestedModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer(allow_null=True)
    photo = PhotoSerializer(many=True)


    def validate(self, data):
        if self.instance is not None:
            instance_user = self.instance.user
            data_user = data.get('user')
            user_fields_for_validation = [
                instance_user.email != data_user['email'],
                instance_user.phone != data_user['phone'],
                instance_user.fam != data_user['last_name'],
                instance_user.name != data_user['name'],
                instance_user.otc != data_user['otc'],
            ]
            if data_user is not None and any(user_fields_for_validation):
                raise serializers.ValidationError(
                    {
                        'Ошибка': 'Данные пользователя заменить нельзя',
                    }
                )
        return data

    class Meta:
        model = Mount
        fields = ['id', 'user', 'beauty_title', 'title', 'other_titles', 'connect', 'coords', 'level', 'photo']
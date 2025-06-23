
from rest_framework import serializers
from .models import User, Coords, Level, MountainPass, Image


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone', 'fam', 'name', 'otc']


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['winter', 'summer', 'autumn', 'spring']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['title', 'image']


class MountainPassSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = MountainPass
        fields = [
            'id', 'beauty_title', 'title', 'other_titles', 'connect',
            'add_time', 'status', 'user', 'coords', 'level', 'images'
        ]
        read_only_fields = ['id', 'add_time', 'status']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        level_data = validated_data.pop('level')
        images_data = validated_data.pop('images')

        # Создаем связанные объекты
        user = User.objects.create(**user_data)
        coords = Coords.objects.create(**coords_data)
        level = Level.objects.create(**level_data)

        # Создаем перевал
        mountain_pass = MountainPass.objects.create(
            user=user,
            coords=coords,
            level=level,
            status='new',
            **validated_data
        )

        # Создаем изображения
        for image_data in images_data:
            Image.objects.create(mountain_pass=mountain_pass, **image_data)

        return mountain_pass
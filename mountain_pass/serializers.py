from rest_framework import serializers
from django.utils.encoding import force_str
from .models import User, Coords, Level, MountainPass, Image


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone', 'fam', 'name', 'otc']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Принудительное преобразование текстовых полей
        for field in ['fam', 'name', 'otc']:
            if field in data and data[field]:
                data[field] = force_str(data[field])
        return data


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']


class LevelSerializer(serializers.ModelSerializer):
    winter = serializers.ChoiceField(choices=Level.LEVEL_CHOICES, required=False, allow_blank=True)
    summer = serializers.ChoiceField(choices=Level.LEVEL_CHOICES, required=False, allow_blank=True)
    autumn = serializers.ChoiceField(choices=Level.LEVEL_CHOICES, required=False, allow_blank=True)
    spring = serializers.ChoiceField(choices=Level.LEVEL_CHOICES, required=False, allow_blank=True)

    class Meta:
        model = Level
        fields = ['winter', 'summer', 'autumn', 'spring']

    def validate(self, data):
        if not any(data.values()):
            raise serializers.ValidationError("Хотя бы один сезон должен быть указан")
        return data


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['title', 'image']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'title' in data:
            data['title'] = force_str(data['title'])
        return data


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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Обрабатываем все текстовые поля
        text_fields = ['beauty_title', 'title', 'other_titles', 'connect']
        for field in text_fields:
            if field in data and data[field]:
                data[field] = force_str(data[field])
        return data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        level_data = validated_data.pop('level')
        images_data = validated_data.pop('images')

        user = User.objects.create(**user_data)
        coords = Coords.objects.create(**coords_data)
        level = Level.objects.create(**level_data)

        mountain_pass = MountainPass.objects.create(
            user=user,
            coords=coords,
            level=level,
            status='new',
            **validated_data
        )

        for image_data in images_data:
            Image.objects.create(mountain_pass=mountain_pass, **image_data)

        return mountain_pass
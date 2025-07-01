import os
from django.core.exceptions import ValidationError
from .models import User, Coords, Level, MountainPass, Image


class DatabaseManager:
    @staticmethod
    def get_db_config():
        return {
            'host': os.getenv('FSTR_DB_HOST', 'localhost'),
            'port': os.getenv('FSTR_DB_PORT', '5432'),
            'login': os.getenv('FSTR_DB_LOGIN', 'postgres'),
            'password': os.getenv('FSTR_DB_PASS', 'postgres'),
        }

    @staticmethod
    def create_mountain_pass(data):
        try:
            # Создаем пользователя
            user_data = data.get('user', {})
            user = User.objects.create(
                email=user_data.get('email'),
                phone=user_data.get('phone'),
                fam=user_data.get('fam'),
                name=user_data.get('name'),
                otc=user_data.get('otc'),
            )

            # Создаем координаты
            coords_data = data.get('coords', {})
            coords = Coords.objects.create(
                latitude=coords_data.get('latitude'),
                longitude=coords_data.get('longitude'),
                height=coords_data.get('height'),
            )

            # Создаем уровень сложности
            level_data = data.get('level', {})
            level = Level.objects.create(
                winter=level_data.get('winter', ''),
                summer=level_data.get('summer', ''),
                autumn=level_data.get('autumn', ''),
                spring=level_data.get('spring', ''),
            )

            # Создаем перевал
            mountain_pass = MountainPass.objects.create(
                beauty_title=data.get('beauty_title', ''),
                title=data.get('title', ''),
                other_titles=data.get('other_titles', ''),
                connect=data.get('connect', ''),
                user=user,
                coords=coords,
                level=level,
                status='new',
            )

            # Добавляем изображения
            images_data = data.get('images', [])
            for image_data in images_data:
                Image.objects.create(
                    mountain_pass=mountain_pass,
                    title=image_data.get('title', ''),
                    image=image_data.get('image'),
                )

            return mountain_pass

        except Exception as e:
            raise ValidationError(f"Ошибка при создании перевала: {str(e)}")

@staticmethod
def update_status(pass_id, new_status):
    try:
        pass_obj = MountainPass.objects.get(id=pass_id)
        if new_status not in dict(MountainPass.STATUS_CHOICES).keys():
            raise ValidationError("Недопустимый статус")
        pass_obj.status = new_status
        pass_obj.save()
        return pass_obj
    except MountainPass.DoesNotExist:
        raise ValidationError("Перевал не найден")

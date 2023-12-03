"""
Сериализаторы для user API
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers


# можно использовать serializers.Serializer
# здесь мы используем ModelSerializer.
# Это позволяет нам автоматически валидировать и сохранять данные в модель,
# которую мы определяем в сериализаторе
class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для объекта пользователя"""

    # здесь определяем модель, поля и дополнительные поля
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']  # здесь определяем только те поля, которые пользователь должен сам установить
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}  # здесь можно определить доп поля валидации без надобности указывать само поле

    def create(self, validated_data):
        """
        Создает и возвращает пользователя с зашифрованными паролем
        По дефолту сериализатор сохранит пароль как чистый текст.
        Нам нужно, чтобы пароль хэшировался, поэтому используем create_user
        """
        return get_user_model().objects.create_user(**validated_data)

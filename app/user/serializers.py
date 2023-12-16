"""
Сериализаторы для user API
"""
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext as _
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


class AuthTokenSerializer(serializers.Serializer):
    """Сериализатор для токена авторизации"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},  # текст по умолчанию прячется с этим input_type
        trim_whitespace=False,  # по умолчанию drf убирает пробелы
    )

    def validate(self, attrs):
        """Валидирует и аутентифицирует пользователя"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )

        if not user:
            msg = _('Не возможно авторизоваться с переданными кредами')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

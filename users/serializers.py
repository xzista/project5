from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    """Полный сериалайзер (для себя)"""

    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "first_name", "last_name"]


class UserPublicSerializer(ModelSerializer):
    """Ограниченный сериалайзер (для чужих профилей)"""

    class Meta:
        model = User
        fields = ["id", "username"]

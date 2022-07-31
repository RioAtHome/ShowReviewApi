from rest_framework import serializers
from .models import ApiUser
from django.core.exceptions import ObjectDoesNotExist


def validate_username(value):
    try:
        ApiUser.objects.get(username=value.lower())
    except ObjectDoesNotExist:
        pass
    else:
        raise serializers.ValidationError("user with this username already exists")

    return value


class ApiUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiUser
        fields = ["username", "password", "role"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validate_username(validated_data["username"])
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance

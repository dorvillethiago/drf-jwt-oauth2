from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )

        if user is None:
            raise serializers.ValidationError("Invalid email or password.")

        attrs["user"] = user
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["name", "email", "password", "provider"]

    def create(self, validated_data):
        user = User(
            name=validated_data["name"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class ProfileSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    picture = serializers.URLField(required=True)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.picture = validated_data.get("picture", instance.picture)
        instance.save()
        return instance

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only= True, min_length=8)
    password2= serializers.CharField(write_only=True)  

    class Meta: 
        model= User
        fields = ["email", "username", "first_name", "last_name", "password", "password2"]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Las contraseñas no coinciden")

        return data

    def create(self, validated_data):
        validated_data.pop("password2")

        return User.objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    followers_count= serializers.ReadOnlyField()
    following_count= serializers.ReadOnlyField()
    is_following= serializers.SerializerMethodField() 

    class Meta: 
        model= User
        fields= [
            "id", "email", "username", "first_name", "last_name", 
            "bio", "department", "position", "followers_count",
            "following_count", "is_following",
        ]
        read_only_fields = ["email"]

    def get_is_following(self, obj):
        request= self.context.get("request") 

        if request and request.user.is_authenticated: 
            return request.user.following.filter(pk=obj.pk).exists() 
        return False

class UserMinimalSerializer(serializers.ModelSerializer):

    class Meta:
        model= User
        fields = ["id", "username", "first_name", "last_name", "position"] 
    



    
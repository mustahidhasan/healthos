from rest_framework import serializers
from django.contrib.auth.models import Group, update_last_login
from django.contrib.auth import authenticate
from .models import *
import json
from rest_framework_jwt.settings import api_settings

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'usr_email', 'first_name', 'last_name',
                  'is_active', 'user_type', ]


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'password', 'usr_email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # print('reg serializer',validated_data)
        user = User.objects.create_user(**validated_data)
        user.username = validated_data['usr_email']
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    usr_email = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=128, write_only=True)

    # token = serializers.CharField(max_length=255, read_only=True)
    # group = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("usr_email", None)
        password = data.get("password", None)
        user = authenticate(usr_email=email, password=password)
        print('user auth: ', user)
        groups = []
        group_list = user.groups.all()

        for group in group_list.iterator():
            print(group)
            groups.append(group.name)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        if user.is_active == 1:
            # print('yes')
            group = Group.objects.get(user=user)
            try:
                payload = JWT_PAYLOAD_HANDLER(user)
                jwt_token = JWT_ENCODE_HANDLER(payload)

                update_last_login(None, user)
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    'User with given email and password does not exists'
                )
            return {
                'email': user.usr_email,
                'token': jwt_token,
                'group': json.dumps(groups),
            }
        else:
            return {
                'email': user.usr_email,
                'token': '',
                'group': '',
            }


    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class CreateCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'user', 'company_name', )


  

from rest_framework import serializers
from django.contrib.auth.models import User

from APP.models import Post


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True, required=True)
    password2 = serializers.CharField(min_length=6, write_only=True, required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'username',  'email', 'first_name',
            'last_name', 'password', 'password2',
        )

    def validate_first_name(self, value):
        if not value.istitle():
            raise serializers.ValidationError("Name must start with uppercase")
        return value

    def validate(self, attrs):
        password2 = attrs.pop('password2')
        if attrs['password'] != password2:
            raise serializers.ValidationError("Password didn't match !")
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data.get('last_name'),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # user = UserSerializer(many=False, read_only=True)



    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'owner', 'like', 'unlike')






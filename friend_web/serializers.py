from django.contrib.auth.models import User
from friend_web.models import Userdata, Connection, CustomUser #GenderType
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.db.models import Q

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ["username", "id", "email"]

class UserDataSerializer(serializers.HyperlinkedModelSerializer):
    Gender_CHOICES = {
        "M": "Cis Gender Male",
        "F": "Cis Gender Female",
        "N": "NonBinary",
        "NA": "Prefer Not To Say"
    }
    username = serializers.StringRelatedField()
    gender = serializers.ChoiceField(choices=Gender_CHOICES)
    headshot = serializers.ImageField()
    class Meta:
        model = Userdata
        fields = ["username", "username_id", "bio", "headshot", "gender",\
        "date_of_birth", "show_horoscope", "instagram_link", "facebook_link", "snapchat_link",\
            "inviteurl", "created_time"]

class PublicUserDataSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.StringRelatedField()
    class Meta:
        model = Userdata
        fields = ["username","headshot", "username_id"]

class UserNameSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField()
    class Meta:
        model = Userdata
        fields = ("username", "username_id")



class ConnectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Connection
        fields = "__all__"


#registration
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email_username = serializers.CharField(required=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TBD remove error messages
        self.fields["email"].required = False
        self.fields["email_username"].required = True

    def validate(self, attrs):

        email_username = attrs.get("email_username")
        password = attrs.get("password")
        if email_username:
            user = get_user_model().objects.filter(Q(email = email_username)|Q(username=email_username)).first()
            if user:
                if user.check_password(password):
                    attrs["user"] = user
                else:
                    msg = "Unable to log in with provided credentials. wrong cridentials"
                    raise serializers.ValidationError(msg)
            else:
                msg = "User with this email address does not exist."
                raise serializers.ValidationError(msg)
        else:
            msg = "Unable to log in with provided credentials. no username caught"
            raise serializers.ValidationError(msg)

        if not user.is_active:
            msg = "User account is disabled."
            raise serializers.ValidationError(msg)

        refresh = self.get_token(user)

        data = {}
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email_is_verified'] = user.email_is_verified
        token['has_data'] = Userdata.objects.filter(username=user).exists()
        return token


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = get_user_model().objects.create(
            email=validated_data["email"],
            username=validated_data["username"],
        )
        user.set_password(validated_data["password"])
        user.save()

        return user

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ("old_password", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data["password"])
        instance.save()

        return instance



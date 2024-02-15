from rest_framework import serializers
from .models import Staff, Fee 
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

class StaffSignUpSerializers(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

    def get_username(self, obj):
        return f"{obj.user.username}"
    
    def get_first_name(self, obj):
        return f"{obj.user.first_name}"
    
    def get_last_name(self, obj):
        return f"{obj.user.last_name}"    
        
    class Meta:
        model = Staff
        fields = ( "username", "first_name", "last_name", "email", "phone_number", "uuid", "id",)


class StaffSignInSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    accessToken = serializers.SerializerMethodField()
    refreshToken = serializers.SerializerMethodField()

    def get_username(self, obj):
            return f"{obj.user.username}"
    
    def get_accessToken(self, obj):
         return f"{AccessToken.for_user(obj)}"
    
    def get_refreshToken(self, obj):
         return f"{RefreshToken.for_user(obj)}"    
    
    class Meta:
        model = Staff
        fields = ( "id", "uuid", "username", "email", "phone_number", "accessToken", "refreshToken", )


class FeesSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
            print(obj, "user info")

            return f"{obj.user.username}" 
        
    class Meta:
          model = Fee
          fields = ("id", "username", "amount", "deadline", "academic_year")


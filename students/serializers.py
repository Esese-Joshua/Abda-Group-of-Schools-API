from rest_framework import serializers
from .models import Students, FeePayment
from staffs.models import Fee  
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

class StudentSignUpSerializers(serializers.ModelSerializer):
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
        model = Students
        fields = ( "fullname", "username",  "email", "faculty", "department", "year_of_admission", "mat_number", "first_name", "last_name", "phone_number", "uuid", "user_id",)



class StudentSignInSerializer(serializers.ModelSerializer):
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
        model = Students
        fields = ( "id", "uuid", "username", "email", "phone_number", "accessToken", "refreshToken", )


class PaystackSerializer(serializers.ModelSerializer):
     class Meta:
          model = FeePayment
          fields = ("id", "payment_status", "payment_ref_no", "amount", "currency", "bank", "fees_id", "user_id", "transaction_date")


# class StudentStudioSerializer(serializers.ModelSerializer):
#      class Meta:
#           model = Studios
#           fields = ("id", "studio_name", "assignment", "grade")


# class FeesSerializer(serializers.ModelSerializer):
#     username = serializers.SerializerMethodField()

#     def get_username(self, obj):
#             return f"{obj.user.username}" 
        
#     class Meta:
#           model = Fee
#           fields = ("id", "username", "amount", "payment_status", "academic_year" )



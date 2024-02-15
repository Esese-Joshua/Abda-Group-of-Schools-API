from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Staff, User, Fee
from django.contrib.auth import authenticate, login

from staffs.serializers import StaffSignUpSerializers, StaffSignInSerializer, FeesSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
import re


# Create your views here.
class StaffRegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data

        if not data:
            return Response(data={"error":"Inappropriate data format"})
        
        first_name = data["first_name"]
        last_name = data["last_name"]
        username = data["username"]
        email = data["email"]
        phone_number = data["phone_number"]
        password = data["password"]
        confirm_password = data["confirm_password"]

        if Staff.objects.filter(email=email).exists():
            return Response(data={"error":"Email already exists!"}, status=status.HTTP_400_BAD_REQUEST)
        
        if password != confirm_password:
            return Response(data={"error":"Passwords does not match!"},  status=status.HTTP_400_BAD_REQUEST)
        
        if User.password == "":
            return Response(data={"error":"Password can't be empty!"},  status=status.HTTP_400_BAD_REQUEST)
        
        user_instance = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
            # email = email,
            password = make_password(password=password)
        )
        user_instance.save()

        if user_instance is None:
            return Response(data={"error":"User instance was not created"}, status=status.HTTP_400_BAD_REQUEST)

        staff_instance = Staff.objects.create(
            user = user_instance,
            email = email,
            phone_number = phone_number
        )
        staff_instance.save()

        if staff_instance is None:
            return Response(data={"error":"Author instance was not created"}, status=status.HTTP_400_BAD_REQUEST)  
        
        serialized_data = StaffSignUpSerializers(instance=staff_instance).data
        return Response(data={"message":"Author registration successful!", "data":serialized_data}, status=status.HTTP_201_CREATED)


class StaffLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data

        username = data["username"]
        password = data["password"]

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            serialized_data = StaffSignInSerializer(instance=user.staff, many=False).data
            return Response(data={"message":f"Login Successful!", "data":serialized_data}, status=status.HTTP_202_ACCEPTED)
        
        return Response(data={"error":f"Invalid login credentials!"}, status=status.HTTP_400_BAD_REQUEST)
    

class CreateFeeView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data

        user = request.user.id
        if user is None:
            return Response(data={"error":"User not recognised! Ensure you are providing accurate student info"}, status=status.HTTP_400_BAD_REQUEST)

        if not data:
            return Response(data={"error":"Inappropriate data format"})
        
        amount = data["amount"]
        deadline = data["deadline"]
        academic_year = data["academic_year"]

        # Validate if all required data fields are provided
        if None in [amount, deadline, academic_year]:
            return Response(data={"error": "Please provide all required data fields"}, status=status.HTTP_400_BAD_REQUEST)

        user_instance = User.objects.get(id=user)

        fees_instance = Fee.objects.create(
            user = user_instance,
            amount = amount,
            deadline = deadline,
            academic_year = academic_year,
        )
        fees_instance.save()

        serialized_data = FeesSerializer(instance=fees_instance).data
        return Response(data={"message":"Fees created successfully!", "data":serialized_data}, status=status.HTTP_201_CREATED)



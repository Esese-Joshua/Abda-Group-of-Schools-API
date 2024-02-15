from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Students, User, FeePayment 
from django.contrib.auth import authenticate, login
from staffs.models import Fee
from staffs.serializers import FeesSerializer
from students.serializers import StudentSignInSerializer, StudentSignUpSerializers, PaystackSerializer 
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
import re, json, requests, datetime
from decouple import config
from django.shortcuts import redirect
from .utility import send_webhook_notification



# Create your views here.
class StudentRegisterView(APIView):
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
        fullname = data["fullname"]
        faculty = data["faculty"]
        department = data["department"]
        year_of_admission = data["year_of_admission"]
        mat_number = data["mat_number"]
        password = data["password"]
        confirm_password = data["confirm_password"] 

        if Students.objects.filter(email=email).exists():
            return Response(data={"error":"Email already exist!"}, status=status.HTTP_400_BAD_REQUEST)
              
        if password != confirm_password:
            return Response(data={"error":"Passowrd does not match!"}, status=status.HTTP_400_BAD_REQUEST)

        if User.password == "":
            return Response(data={"error":"Password cannot be empty!"}, status=status.HTTP_400_BAD_REQUEST)

        user_instance = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
            password = make_password(password=password)
        )
        user_instance.save()

        if user_instance is None:
            return Response(data={"error":"User instance was not created"}, status=status.HTTP_400_BAD_REQUEST)

        students_instance = Students.objects.create(
            user = user_instance,
            phone_number = phone_number,
            email = email,
            fullname = fullname,
            faculty = faculty,
            department = department,
            year_of_admission = year_of_admission,
            mat_number = mat_number,
        )
        students_instance.save()

        if students_instance is None:
            return Response(data={"error":"Author instance was not created"}, status=status.HTTP_400_BAD_REQUEST)  
        
        serialized_data = StudentSignUpSerializers(instance=students_instance).data
        return Response(data={"message":"Author registration successful!", "data":serialized_data}, status=status.HTTP_201_CREATED)


class StudentLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data

        username = data["username"]
        password = data["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            serialized_data = StudentSignInSerializer(instance=user.students, many=False).data
            return Response(data={"message":f"Login Successful! Welcome {user.username}", "data":serialized_data}, status=status.HTTP_202_ACCEPTED)
        
        return Response(data={"error":f"Invalid login credentials!"}, status=status.HTTP_400_BAD_REQUEST)
    
    
# class StudentStudioView(APIView):
#     permission_classes = [AllowAny]
#     def post(self, request):
#         data = request.data

#         if not data:
#             return Response(data={"error":"Inappropriate data format"})
        
#         studio_name = data["studio_name"]
#         assignment = data["assignment"]
#         grade = data["grade"] 
        
#         student_instance = Students.objects.get(uuid=data["uuid"])

#         studio_instance = Studios.objects.create(
#             student = student_instance,
#             studio_name = studio_name,
#             assignment = assignment,
#             grade = grade,
#         )         

#         if studio_instance is None:
#             return Response(data={"error":"Studio was not registered! Check again"}, status=status.HTTP_400_BAD_REQUEST)

#         studio_instance.save()

#         serialized_data = StudentStudioSerializer(instance=studio_instance).data
#         return Response(data={"message":"Studio registration successful!", "data":serialized_data}, status=status.HTTP_201_CREATED)



class FessByAcademicYearView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        academic_year :dict = request.GET.get("academic_year",None)
         
        if academic_year is None:
           return Response(data={"error":"Academic session can't be empty. Please Provide a valid academic year!"}, status=status.HTTP_400_BAD_REQUEST)

        fees = Fee.objects.filter(academic_year=academic_year)

        serialized_data = PaystackSerializer(instance=fees, many=True).data  
        return Response(data={"data":serialized_data}, status=status.HTTP_200_OK)


class FeePaymentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        academic_year = request.GET.get("academic_year", None)

        if academic_year is None:
            return Response(data={"error": "Academic session can't be empty. Please provide a valid academic year!"}, status=status.HTTP_400_BAD_REQUEST)

        fees = Fee.objects.filter(academic_year=academic_year)
        student = Students.objects.get(id=request.user.id)
 
        if fees.exists():
            for fee in fees:
                amount = fee.amount
                email = student.email

                # Connect to Paystack
                curl = "https://api.paystack.co/transaction/initialize" 
                headers = {"Content-Type": "application/json", "Authorization": f"Bearer {config('PAYSTACK_SECRET_KEY')}"}

                data = {
                    "amount": amount * 100,
                    "email": email,
                    # "callback_url": "http://127.0.0.1:8000/paystacklanding?reference=fxstygffxdt",
                    "callback_url" : "http://127.0.0.1:8000/student/paystack/webhook/"
                }      
                response = requests.post(curl, headers=headers, data=json.dumps(data))
                json_response = response.json()

                if response.status_code == 200:
                    reference = response.json().get("data").get("reference")

                    #Create a new FeePayment record on db
                    FeePayment.objects.create(
                        user_id = request.user.id,
                        fees_id = fee.id,
                        payment_ref_no = reference, 
                        payment_status = "PENDING"
                        )

                    authorization_url = response.json().get("data").get("authorization_url")

                    return Response({"amount":amount, "email":email, "payment_reference":reference, "authorization":authorization_url}, status=status.HTTP_200_OK)
                else:
                    return Response(json_response)
        else:
            return Response({"error": "Fee is not found!"}, status=status.HTTP_404_NOT_FOUND)
        

class PaystackCallView(APIView):
    def get(self, request):
        reference : str = request.GET.get("reference", None)
        trxref : str = request.GET.get("trxref")        
        return Response(data={"data":f" Transaction was successful! Transaction references are: {reference} {trxref}"}, status=status.HTTP_200_OK)


class PaystackLandingView(APIView):
    def get(self, request):       
        reference :dict = request.GET.get("reference", None)
        
        if reference is None:
           return Response(data={"error":"Academic session can't be empty. Please Provide a valid academic year!"}, status=status.HTTP_400_BAD_REQUEST)

        #connect to paystack                                         
        headers = {"Content-Type":"application/json","Authorization":f"Bearer {config('PAYSTACK_SECRET_KEY')}"}
        verifyurl = f"https://api.paystack.co/transaction/verify/{reference}" 

        response = requests.get(verifyurl, headers=headers)  

        if response.status_code == 200:
            if response.json().get("data").get("status") == "success":
                #update a new FeePayment record 
                FeePayment.objects.filter(payment_ref_no=reference).update(payment_status = "PAID",
                                                                           transaction_date = response.json().get("data").get("paid_at"),
                                                                           amount = response.json().get("data").get("amount"),
                                                                           currency = response.json().get("data").get("currency"),
                                                                           card_type = response.json().get("data").get("authorization").get("card_type"),
                                                                           channel = response.json().get("data").get("authorization").get("channel"),
                                                                           bank = response.json().get("data").get("authorization").get("bank"),
                                                                           bin = response.json().get("data").get("authorization").get("bin"),
                                                                           authorization_code = response.json().get("data").get("authorization").get("authorization_code"),
                                                                           last4 = response.json().get("data").get("authorization").get("last4"),
                                                                           )

                # Send webhook notification
                webhook_url = "https://webhook.site/67d0c0be-fbdf-4d90-b3e4-dedad1f96911"                    
                response = send_webhook_notification(webhook_url, request)
    
                if response:               
                 return Response({"response":response}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Payment was not successful."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Failed to verify payment"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class PaymentDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, payment_ref_no):
        fee_payment = FeePayment.objects.get(payment_ref_no=payment_ref_no)

        serializer_data = PaystackSerializer(instance=fee_payment, many=False).data
        return Response(data={"data":serializer_data}, status=status.HTTP_200_OK)
    

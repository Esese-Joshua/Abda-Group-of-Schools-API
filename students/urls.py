from django.urls import path
from .views import StudentRegisterView, StudentLoginView, FessByAcademicYearView, FeePaymentView, PaystackLandingView, PaymentDetailsView

app_name = "students"

urlpatterns = [
    path("sign-up/", StudentRegisterView.as_view(), name="sign-up"),
    path("sign-in/", StudentLoginView.as_view(), name="sign-up"),
    # path("studio/", StudentStudioView.as_view(), name="studio")
    path("fees/", FessByAcademicYearView.as_view(), name="fees"),       
    path("fee-payment/", FeePaymentView.as_view(), name="fee-payment"), 
    path("paystack/webhook/", PaystackLandingView.as_view(), name="paystack_webhook"),  
    path("view-payment/<str:payment_ref_no>", PaymentDetailsView.as_view(), name="view-payment"), 
]

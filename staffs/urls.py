from django.urls import path
from .views import StaffRegisterView, StaffLoginView, CreateFeeView

app_name = "staffs"

urlpatterns = [
    path("sign-up/", StaffRegisterView.as_view(), name="sign-up"),
    path("sign-in/", StaffLoginView.as_view(), name="sign-in"),
    path("fees/", CreateFeeView.as_view(), name="fees"),

]

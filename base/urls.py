from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("staff/", include("staffs.urls")),
    path("student/", include("students.urls")),
    # path("paystacklanding/", include("students.urls")),

]

from django.db import models
from staffs.models import User, Fee
import random, uuid
from django.core.validators import EmailValidator
import uuid
# Create your models here.

class Students(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField(null=False)
    email = models.EmailField(validators=[EmailValidator()], unique=True)
    fullname = models.CharField(null=True, blank=False, max_length=100)
    faculty = models.CharField(null=False, max_length=50)
    department = models.CharField(null=False, max_length=50)
    year_of_admission = models.DateField(null=False)
    mat_number = models.CharField(null=False,editable=False, unique=True, max_length=50)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    def generate_mat_number(faculty, department, year_of_admission):
        random_number = random.randint(100000, 999999)
        length = str(random_number).zfill(10)    
        return f"{faculty[:3]}/{department[:3]}/{year_of_admission[-2]}/{length}"

    def save(self, *args, **kwargs):
            if not self.mat_number:
                self.mat_number = self.generate_mat_number()
            super(Students, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.mat_number}"
    

# class Studios(models.Model):
#      student = models.ForeignKey(Students, on_delete=models.CASCADE)
#      studio_name = models.CharField(max_length=50)
#      assignment = models.CharField(max_length=50)               
#      grade = models.CharField(max_length=50)
#     #  uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

#      def __str__(self):
#          return self.studio_name
     

class FeePayment(models.Model):
     PAYMENT_STATUS_CHOICES = [
        # the first element "PAID" is the value, while the second element will be displayed in tha admin panal
        ('PAID', 'Paid'),
        ('NOT_PAID', 'Not Paid'),
        ('PENDING', 'Pending')
    ]

     user = models.ForeignKey(User, on_delete=models.CASCADE)
     fees = models.ForeignKey(Fee, on_delete=models.CASCADE, default=1000)
     payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default="PENDING")
     payment_ref_no = models.CharField(max_length=50, default=1000)   
     transaction_date = models.DateTimeField(null=True)
     amount = models.IntegerField(default=0, null=True)
     currency = models.CharField(max_length=50, null=True)
     card_type = models.CharField(max_length=50, null=True)
     channel = models.CharField(max_length=50, null=True)
     bank = models.CharField(max_length=50, null=True)
     bin = models.CharField(max_length=50, null=True)
     authorization_code = models.CharField(max_length=50, null=True)
     last4 = models.CharField(max_length=50, null=True)
     
     def generate_payment_ref_no(self):
          random_number = random.randint(1000, 9999)
          length = str(random_number).zfill(10)
          return f"{self.user.username[:3]}/{length}"
     

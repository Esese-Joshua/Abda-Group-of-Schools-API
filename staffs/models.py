from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
import uuid


# Create your models here.
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(validators=[EmailValidator()], unique=True)
    phone_number = models.CharField(null=False, max_length=30)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    def save(self, *args, **kwargs):
        self.uuid = uuid.uuid4()
        super(Staff, self).save(*args, **kwargs)    
   
    def __str__(self):
        return f"{self.uuid}"
    

class Fee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    deadline = models.DateField()
    academic_year = models.CharField(max_length=50)


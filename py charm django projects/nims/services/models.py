from django.db import models


class Service(models.Model):
    categeory = models.CharField(max_length=250)
    fee= models.DecimalField(max_digits=5,decimal_places=2)
    categeory_pic =models.CharField(max_length=1000)
    def __str__(self):
        return self.categeory

class Doctor(models.Model):
    service=models.ForeignKey(Service,on_delete=models.CASCADE)
    name=models.CharField(max_length=250)
    qualification =models.CharField(max_length=250)
    experience =models.CharField(max_length=100)
    doctor_pic = models.CharField(max_length=1000)
    def __str__(self):
        return self.name

from django.db import models
import datetime
from django import utils

#the reigon stands for villages, towns, cities, provinces, countries....
class Region(models.Model):
    region_address = models.CharField(max_length=30, blank=False)
    # super region is the level above, for example
    # Erbil is super place of Soran, and Soran is super region for Hariq Street
    super_region = models.ForeignKey('Region',on_delete=models.CASCADE, blank=True,null=True)
    def __str__ (self):
        if self.super_region==None:
            return self.region_address
        else:
            return "%s, %s"%(self.region_address,self.super_region)

#the Disease class stands for items of Disease
class Disease(models.Model):
    disease = models.CharField(max_length=30)
    def __str__(self):
        return self.disease

class Sign(models.Model):
    sign = models.CharField(max_length=30)
    def __str__(self):
        return self.sign

# Create your models here.
class Patient(models.Model):
    full_name = models.CharField(max_length=30, blank=True)
    case_number = models.SlugField(default='')
    BLOOD_GROUPS = (
        (0, 'Not Specified'),(1, 'A+'),(2, 'B+'),(3, 'AB+'),(4, 'O+'),
        (5, 'A-'),(6, 'B-'),(7, 'AB-'),(8, 'O-'))
    blood_group = models.PositiveSmallIntegerField(choices=BLOOD_GROUPS,default=0)
    occupation = models.CharField(max_length=30, blank=True,null=True)
    address = models.ForeignKey('Region',on_delete=models.CASCADE,blank=True,null=True)
    mobile = models.CharField(max_length=30, blank=True,null=True)
    date_of_birth = models.DateField(default=utils.timezone.now)
    GENDERS = ((0,'Not Specified'),(1,'Male'),(2,'Female'))
    gender = models.PositiveSmallIntegerField(choices=GENDERS,default=0)
    date_of_infection = models.DateField(default=utils.timezone.now)

    source = models.ForeignKey('Patient',on_delete=models.CASCADE, blank=True,null=True)
    other_source = models.CharField(max_length=30, blank=True,null=True)
    CONDITIONS = (
        (0, 'Not Specified'),(1, 'Fully Recovered'),(2, 'Under Treatment'),
        (3, 'Serious'),(4, 'Dead'))
    condition = models.PositiveSmallIntegerField(choices=CONDITIONS,default=0)

    diseases = models.ManyToManyField('Disease',blank=True)
    signs = models.ManyToManyField('Sign',blank=True)
    def age(self):
        return utils.timezone.now.year - self.date_of_birth.year

    def __str__ (self):
        return "%d.%s"%(self.age,self.address)

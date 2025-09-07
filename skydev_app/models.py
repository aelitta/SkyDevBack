from django.db import models
from .choices import *

# Create your models here.
class Domain(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    code = models.IntegerField()


class Vacancy(models.Model):
    status = models.IntegerField(choices=VACANCY_STATUSES)
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contract_type = models.IntegerField(choices=CONTRACT_STATUSES)
    emp_type = models.IntegerField(choices=EMP_STATUSES)
    work_sced = models.IntegerField(choices=WS_STATUSES)
    income = models.IntegerField()
    salary_max = models.IntegerField()
    salary_min = models.IntegerField()
    ann_premium = models.IntegerField()
    premium_type = models.IntegerField(choices=PREMIUM_TYPE_STATUSES)
    edu_level = models.IntegerField(choices=EDU_LEVEL_STATUSES)
    experience = models.IntegerField()
    software_knowledges = models.CharField(max_length=255)
    software_skills = models.CharField(max_length=255)
    foreign_langs = models.CharField(max_length=255)
    allow_trip = models.IntegerField(choices=AT_STATUSES)
    change_date = models.DateTimeField()


class VacancyReq(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    whois = models.CharField(max_length=255, null=True)
    duties = models.TextField()
    requirements = models.TextField()


class Candidate(models.Model):
    fio = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    contacts = models.TextField()
    status = models.IntegerField(choices=AVA_STATUSES)
    photo = models.ImageField()
    foreign_langs = models.CharField(max_length=255)


class EmpProfile(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    specs = models.TextField()
    contract_type = models.IntegerField(choices=CONTRACT_STATUSES)
    emp_type = models.IntegerField(choices=EMP_STATUSES)
    work_sced = models.IntegerField(choices=WS_STATUSES)
    software_knowledges = models.CharField(max_length=255)
    software_skills = models.CharField(max_length=255)
    allow_trip = models.IntegerField(choices=AT_STATUSES)



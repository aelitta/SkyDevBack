from django.contrib import admin

# Register your models here.

from django.contrib import admin

# Register your models here.
from .models import Vacancy,Candidate, EmpProfile, VacancyReq

#admin.site.register(Project)

class VacancyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status')
    list_display_links = ['name']

admin.site.register(Vacancy,VacancyAdmin)

class VacancyReqAdmin(admin.ModelAdmin):
    list_display = ('vacancy', 'whois', 'duties', 'requirements')
    list_display_links = ['whois']

admin.site.register(VacancyReq,VacancyReqAdmin)


class CandidateAdmin(admin.ModelAdmin):
    list_display = ('id', 'fio', 'status', 'photo')
    list_display_links = ['fio']

admin.site.register(Candidate, CandidateAdmin)


class EmpProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'candidate', 'specs')
    list_display_links = ['candidate']

admin.site.register(EmpProfile, EmpProfileAdmin)

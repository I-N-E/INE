from django.contrib import admin
from .models import Idea,SubIdea,DataUser

# Register your models here.
admin.site.register(Idea)
admin.site.register(SubIdea)
admin.site.register(DataUser)

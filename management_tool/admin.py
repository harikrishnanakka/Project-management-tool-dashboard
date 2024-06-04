from django.contrib import admin

# Register your models here.
from .models import CustomUser, Project, Task, Assignment

admin.site.register(CustomUser)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Assignment)
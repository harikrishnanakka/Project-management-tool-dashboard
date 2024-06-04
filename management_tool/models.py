


from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLES = (
        ('PM', 'Project Manager'),
        ('TM', 'Team Member'),
        ('CL', 'Client'),
    )
    role = models.CharField(max_length=2, choices=ROLES)
    
    def __str__(self):
        return self.username
    
    
    
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return self.name
    
    

class Task(models.Model):
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=(('done', 'Done'), ('pending', 'Pending')))
    deadline = models.DateField()
    
    
    def __str__(self):
        return self.name

class Assignment(models.Model):
    task = models.ForeignKey(Task, related_name='assignments', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(CustomUser, related_name='assignments', on_delete=models.CASCADE)
    comment = models.TextField()
    
    def __str__(self):
        return f'{self.task.name} -> {self.assigned_to.username}'




    





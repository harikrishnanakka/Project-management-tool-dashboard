from django.urls import path
from management_tool import views




urlpatterns = [
    path('api/projects/<int:id>/progress/',views.progress,name="progress")
    
]
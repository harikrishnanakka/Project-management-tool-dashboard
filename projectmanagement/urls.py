from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView
from management_tool import views
from management_tool.views import CustomAuthToken, LogoutView,UserRegistrationView
from rest_framework.authtoken.views import obtain_auth_token
import logging

# Configure logging
logger = logging.getLogger(__name__)

router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet, basename='project')
router.register(r'tasks', views.TaskViewSet, basename='task')
router.register(r'assignments', views.AssignmentViewSet, basename='assignment')
router.register(r'users', views.UserViewSet, basename='user')

logger.debug("URL patterns being registered")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', CustomAuthToken.as_view(), name='api-token-auth'),
    path('api-token-logout/', LogoutView.as_view(), name='api-token-logout'),
    path('api/register/', UserRegistrationView.as_view(), name='user-register'),
    path('api/', include(router.urls)),
    path('calender/', views.calender, name='calender'),
    path('payments/', views.payments, name='payments'),
    path('filings/', views.filings, name='filings'),
    path('conversations/', views.conversations, name='conversations'),
    path('settings/', views.settings, name='settings'),
    re_path('', TemplateView.as_view(template_name='index.html')),
   
]



logger.debug("URL patterns registered: %s", urlpatterns)
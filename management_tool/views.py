from django.shortcuts import render
from rest_framework import viewsets
from .models import Project, Task, Assignment, CustomUser
from .serializers import ProjectSerializer, TaskSerializer, AssignmentSerializer, UserSerializer,CustomAuthTokenSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsProjectManager, IsTeamMember, IsClient
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny
import logging
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# The ProjectViewSet class is a viewset for the Project model. It provides CRUD operations for projects.
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly | (IsProjectManager | IsTeamMember | IsClient)]

    # The progress method is an action that returns the progress of a project based on the completed tasks.
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticatedOrReadOnly |IsProjectManager | IsTeamMember])
    def progress(self, request, pk=None):
        project = self.get_object()
        tasks = Task.objects.filter(project=project)
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status='done').count()
        progress = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        return Response({'progress': progress})

# The create, update, and destroy methods are overridden to check if the user is a project manager before allowing the operation.

    def create(self, request, *args, **kwargs):
        if not request.user.role == 'PM':
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if not request.user.role == 'PM':
            return Response(status=status.HTTP_403_FORBIDDEN)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.role == 'PM':
            return Response(status=status.HTTP_403_FORBIDDEN)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# The TaskViewSet class is a viewset for the Task model. It provides CRUD operations for tasks.
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedOrReadOnly | (IsProjectManager | IsTeamMember)]
    
 # The get_queryset method is overridden to filter tasks based on a project_id query parameter.   
    def get_queryset(self):
        project_id = self.request.query_params.get('project_id', None)
        if project_id:
            return Task.objects.filter(project_id=project_id)
        return super().get_queryset()

# The update_status method is an action that updates the status of a task.
    @action(detail=True, methods=['post'], permission_classes=[IsProjectManager | IsTeamMember])
    def update_status(self, request, pk=None):
        task = self.get_object()
        task.status = request.data.get('status')
        task.save()
        return Response({'status': 'status updated'})

   # The create, update, and destroy methods are overridden to check if the user is a project manager or team member before allowing the operation. 
    def create(self, request, *args, **kwargs):
        if not request.user.role == 'PM':
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if not request.user.role == 'PM':
            return Response(status=status.HTTP_403_FORBIDDEN)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.role == 'PM':
            return Response(status=status.HTTP_403_FORBIDDEN)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)



# The AssignmentViewSet class is a viewset for the Assignment model. It provides CRUD operations for assignments.
class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly | (IsProjectManager | IsTeamMember)]

# The UserViewSet class is a viewset for the CustomUser model. It provides CRUD operations for users.
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsProjectManager]








# The CustomAuthToken class is an APIView that handles authentication token creation.
logger = logging.getLogger(__name__)

# It uses the CustomAuthTokenSerializer to validate the request data and create an authentication token for the user.
class CustomAuthToken(APIView):
    
    authentication_classes = ()
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        logger.debug("CustomAuthToken POST request received")
        serializer = CustomAuthTokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.pk, 'role': user.role})


# The LogoutView class is an APIView that handles user logout.
# It deletes the authentication token for the user and logs the user out.
class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        request.auth.delete()
        logout(request)
        return Response(status=status.HTTP_200_OK)




# The calender, settings, payments, filings, and conversations functions are views that render HTML templates for different pages.
def calender(request):
    return render(request,'calender.html')


def settings(request):
    return render(request,'settings.html')

def payments(request):
    return render(request,'payments.html')

def filings(request):
    return render(request,'filings.html')

def conversations(request):
    return render(request,'conversations.html')



from .serializers import UserRegistrationSerializer

class UserRegistrationView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

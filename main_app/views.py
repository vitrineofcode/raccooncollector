from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import generics, status, permissions
from .models import Raccoon, Feeding, Exercise
from .serializers import RaccoonSerializer, FeedingSerializer, ExerciseSerializer, UserSerializer

# User Registration
class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    user = User.objects.get(username=response.data['username'])
    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': response.data
    })
  
# User Login
class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

  # User Verification
class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = User.objects.get(username=request.user)  # Fetch user profile
    refresh = RefreshToken.for_user(request.user)  # Generate new refresh token
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data
    })

# Create your views here.
class Home(APIView):
  # Define a get method that returns a welcome message
  def get(self, request):
    content = {'message': 'Welcome to the raccoon collector API!'}
    return Response(content)
  
class RaccoonList(generics.ListCreateAPIView):
  serializer_class = RaccoonSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
      # This ensures we only return raccoons belonging to the logged-in user
      user = self.request.user
      return Raccoon.objects.filter(user=user)

  def perform_create(self, serializer):
      # This associates the newly created raccoon with the logged-in user
      serializer.save(user=self.request.user)

class ExerciseList(generics.ListCreateAPIView):
  queryset = Exercise.objects.all()
  serializer_class = ExerciseSerializer 

class RaccoonDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = RaccoonSerializer
  lookup_field = 'id'

  def get_queryset(self):
    user = self.request.user
    return Raccoon.objects.filter(user=user)

  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)

    exercises_not_associated = Exercise.objects.exclude(id__in=instance.exercises.all())
    exercises_serializer = ExerciseSerializer(exercises_not_associated, many=True)

    return Response({
        'raccoon': serializer.data,
        'exercises_not_associated': exercises_serializer.data
    })

  def perform_update(self, serializer):
    raccoon = self.get_object()
    if raccoon.user != self.request.user:
        raise PermissionDenied({"message": "You do not have permission to edit this raccoon."})
    serializer.save()

  def perform_destroy(self, instance):
    if instance.user != self.request.user:
        raise PermissionDenied({"message": "You do not have permission to delete this raccoon."})
    instance.delete()
  

class ExerciseDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Exercise.objects.all()
  serializer_class = ExerciseSerializer
  lookup_field = 'id'

class FeedingListCreate(generics.ListCreateAPIView):
  serializer_class = FeedingSerializer

  def get_queryset(self):
    raccoon_id = self.kwargs['raccoon_id']
    return Feeding.objects.filter(raccoon_id=raccoon_id)

  def perform_create(self, serializer):
    raccoon_id = self.kwargs['raccoon_id']
    raccoon = Raccoon.objects.get(id=raccoon_id)
    serializer.save(raccoon=raccoon)

class FeedingDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = FeedingSerializer
  lookup_field = 'id'

  def get_queryset(self):
    raccoon_id = self.kwargs['raccoon_id']
    return Feeding.objects.filter(raccoon_id=raccoon_id)
  
class AddExerciseToRaccoon(APIView):
  def post(self, request, raccoon_id, exercise_id):
    raccoon = Raccoon.objects.get(id=raccoon_id)
    exercise = Exercise.objects.get(id=exercise_id)
    raccoon.exercises.add(exercise)
    return Response({'message': f'Exercise {exercise.name} added to Raccoon {raccoon.name}'})
  
class RemoveExerciseFromRaccoon(APIView):
  def post(self, request,raccoon_id , exercise_id):
    raccoon = Raccoon.objects.get(id=raccoon_id)
    exercise = Exercise.objects.get(id=exercise_id)
    raccoon.exercises.remove(exercise)
    return Response({'message': f'Exercise {exercise.name} removed from Raccoon {raccoon.name}'})


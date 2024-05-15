from rest_framework import serializers
from .models import Raccoon, Feeding, Exercise
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)

  class Meta:
    model = User
    fields = ['id', 'username', 'email', 'password']

  def create(self, validated_data):
    user = User.objects.create_user(
      username=validated_data['username'],
      email=validated_data['email'],
      password=validated_data['password']
    )

    return user

class ExerciseSerializer(serializers.ModelSerializer):
  class Meta:
    model = Exercise
    fields = '__all__'

class RaccoonSerializer(serializers.ModelSerializer):
  fed_for_today = serializers.SerializerMethodField()
  exercise = ExerciseSerializer(many=True, read_only=True)
  user = serializers.PrimaryKeyRelatedField(read_only=True)

  class Meta:
    model = Raccoon
    fields = '__all__'

  def get_fed_for_today(self, obj):
    return obj.fed_for_today()

class FeedingSerializer(serializers.ModelSerializer):
  class Meta:
    model = Feeding
    fields = '__all__'
    read_only_fields = ['raccoon']
  
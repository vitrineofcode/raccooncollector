from django.urls import path
from .views import Home, RaccoonList, RaccoonDetail, FeedingListCreate, FeedingDetail, ExerciseList, ExerciseDetail, AddExerciseToRaccoon, RemoveExerciseFromRaccoon, CreateUserView, LoginView, VerifyUserView

urlpatterns = [
  # Define the home path
  path('', Home.as_view(), name='home'),
  path('raccoons/', RaccoonList.as_view(), name='raccoon_list'),
  path('raccoons/<int:id>/', RaccoonDetail.as_view(), name='raccoon_detail'),
  path('raccoons/<int:raccoon_id>/feedings/', FeedingListCreate.as_view(), name='feeding-list-create'),
	path('raccoons/<int:raccoon_id>/feedings/<int:id>/', FeedingDetail.as_view(), name='feeding-detail'),
  path('exercises/', ExerciseList.as_view(), name='exercise_list'),
  path('exercises/<int:id>/', ExerciseDetail.as_view(), name='exercise_detail'),
  path('raccoons/<int:raccoon_id>/add_exercise/<int:exercise_id>/', AddExerciseToRaccoon.as_view(), name='add-exercise-to-raccoon'),
  path('raccoon/<int:raccoon_id>/remove_exercise/<int:exercise_id>/', RemoveExerciseFromRaccoon.as_view(), name='remove-exercise-from-raccoon'),
  path('users/register/', CreateUserView.as_view(), name='register'),
  path('users/login/', LoginView.as_view(), name='login'),
  path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
]
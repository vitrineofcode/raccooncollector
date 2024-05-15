from django.db import models
from datetime import date
from django.contrib.auth.models import User

# A tuple of 2-tuples
MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

# Add the Exercise model
class Exercise(models.Model):
  name = models.CharField(max_length=50)
  difficulty = models.CharField(max_length=20)

  def __str__(self):
    return self.name


# Create your models here.
class Raccoon(models.Model):
  name = models.CharField(max_length=100)
  color = models.CharField(max_length=100)
  age = models.IntegerField()
  description = models.TextField(max_length=250)
  exercises = models.ManyToManyField(Exercise)
  # user = models.ForeignKey(User, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE, default='')



  def __str__(self):
    return self.name
  
  def fed_for_today(self):
    return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)
  
class Feeding(models.Model):
  date = models.DateField('Feeding Date')
  meal = models.CharField(
    max_length=1,
    # add the 'choices' field option
    choices=MEALS,
    # set the default value for meal to be 'B'
    default=MEALS[0][0]
  )
  raccoon = models.ForeignKey(Raccoon, on_delete=models.CASCADE)
  def __str__(self):
    # Nice method for obtaining the friendly value of a Field.choice
    return f"{self.get_meal_display()} on {self.date}"
  # change the default sort
  class Meta:
    ordering = ['-date']
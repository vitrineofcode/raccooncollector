from django.contrib import admin

# Register your models here.
from .models import Raccoon, Feeding, Exercise

# Register the Raccoon model with the admin site
admin.site.register(Raccoon)
# Register the Feeding model with the admin site
admin.site.register(Feeding)
# Register the Exercise model with the admin site
admin.site.register(Exercise)

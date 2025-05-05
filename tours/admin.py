from django.contrib import admin
from .models import Tour, Registration

admin.site.register(Tour)
admin.site.register(Registration)
from .models import TourGuide

@admin.register(TourGuide)
class TourGuideAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone')
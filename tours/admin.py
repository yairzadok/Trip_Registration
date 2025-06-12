from django.contrib import admin
from .models import Tour, Registration

admin.site.register(Tour)
admin.site.register(Registration)
from .models import TourGuide

@admin.register(TourGuide)
class TourGuideAdmin(admin.ModelAdmin):
    list_display = ('tour_guide_first_name', 'tour_guide_last_name', 'tour_guide_email', 'tour_guide_phone')
from django.contrib import admin
from django.urls import path
from tours import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/<int:tour_id>/', views.register, name='register'),
    path('success/', views.success, name='success'),
    path('registrations/', views.registration_list, name='registration_list'),
    path('export_registrations/', views.export_registrations_excel, name='export_registrations'),
    path('delete_registration/<int:registration_id>/', views.delete_registration, name='delete_registration'),
    path('toggle_attendance/<int:registration_id>/', views.toggle_attendance, name='toggle_attendance'),
    path('send_reminders/', views.send_reminder_emails, name='send_reminders'),
    path('participants/', views.participants_list, name='participants_list'),
     path('participants/<int:tour_id>/', views.participants_list, name='participants_list'),
    path('update_presence/', views.update_presence, name='update_presence'),
    path('send-attendance-report/', views.send_attendance_report, name='send_attendance_report'),
    path('register-guide/', views.register_tour_guide, name='register_guide'),
    path('thanks/', views.thank_you, name='guide_thank_you'),
    ]

# טיפול בקבצי מדיה בזמן פיתוח
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

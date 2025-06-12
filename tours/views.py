from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Tour, Registration, TourGuide
from .forms import RegistrationForm
from django.core.mail import EmailMultiAlternatives
from django.core.mail.message import make_msgid, EmailMessage
from email.mime.image import MIMEImage
import qrcode
import openpyxl
import io
from PIL import Image, ImageDraw, ImageFont
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.core.mail import send_mass_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from email.utils import make_msgid
from .forms import TourForm
import os
from django.conf import settings


@csrf_exempt
def update_presence(request):
    if request.method == "POST":
        registration_id = request.POST.get('id')
        is_present = request.POST.get('present') == 'true'

        registration = get_object_or_404(Registration, id=registration_id)
        registration.נוכחות = is_present
        registration.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

def home(request):
    tours = Tour.objects.all().order_by('-id')  # הצגת הסיורים החדשים תחילה
    return render(request, 'travelers/home.html', {'tours': tours})



def export_registrations_excel(request):
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="registrations.xlsx"'

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "נרשמים"

    # הוספת כותרות
    sheet.append(['שם פרטי', 'שם משפחה', 'טלפון', 'אימייל', 'נוכחות'])

    # הוספת הנתונים
    for registration in Registration.objects.all():
        sheet.append([
            registration.שם_פרטי,
            registration.שם_משפחה,
            registration.טלפון,
            registration.אימייל,
            'הגיע' if registration.נוכחות else 'לא הגיע',
        ])

    workbook.save(response)
    return response
def registration_list(request):
    tours = Tour.objects.prefetch_related('registrations').all()
    return render(request, 'travelers/registration_list.html', {'tours': tours})

from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm
from .models import Tour

def register(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.סיור = tour
            registration.save()
            # כאן ההפניה לדף הסליקה
            return redirect('payment_redirect')  # השם מה-urls.py

    else:
        form = RegistrationForm()

    return render(request, 'travelers/traveler_register.html', {'form': form, 'tour': tour})


# בתוך הקובץ: tours/views.py

def payment_redirect(request):
    return render(request, 'travelers/payment_redirect.html')


def success(request):
    return render(request, 'travelers/success.html')

def generate_qr_with_text(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    width, height = qr_img.size
    total_height = height + 50
    new_img = Image.new("RGB", (width, total_height), "white")
    new_img.paste(qr_img, (0, 0))

    draw = ImageDraw.Draw(new_img)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    # הפוך את הטקסט
    text = "אנא הצג קוד זה למדריך"
    reversed_text = text[::-1]

    bbox = draw.textbbox((0, 0), reversed_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (width - text_width) // 2
    text_y = height + 10
    draw.text((text_x, text_y), reversed_text, font=font, fill="black")

    qr_io = io.BytesIO()
    new_img.save(qr_io, format='PNG')
    qr_io.seek(0)
    return qr_io


def delete_registration(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id)
    registration.delete()
    return redirect('registration_list')

def toggle_attendance(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id)
    registration.נוכחות = not registration.נוכחות
    registration.save()
    return redirect('registration_list')

def send_reminder_emails(request):
    tour = Tour.objects.first()
    registrations = Registration.objects.all()

    subject = f"תזכורת לסיור: {tour.כותרת_ראשית}"
    message = f"""שלום,
זוהי תזכורת לסיור "{tour.כותרת_ראשית}" שיתקיים בתאריך {tour.תאריך} בשעה {tour.שעת_התחלה}.
מיקום: {tour.מיקום}.

מחכים לראותך!
"""

    from_email = 'your_email@gmail.com'  # עדכן כאן את האימייל שלך

    datatuple = [
        (subject, message, from_email, [registration.אימייל])
        for registration in registrations
    ]

    send_mass_mail(datatuple, fail_silently=False)

    return redirect('registration_list')

def participants_list(request):
    tour_id = request.GET.get('tour_id')
    if tour_id:
        registrations = Registration.objects.filter(סיור_id=tour_id)
    else:
        registrations = Registration.objects.all()  # גיבוי למקרה שאין פילטר
    return render(request, 'travelers/participants_list.html', {'registrations': registrations})


@csrf_exempt
def send_attendance_report(request):
    if request.method == 'POST':
        tour_guide_email = request.POST.get('tour_guide_email')

        if not tour_guide_email:
            return JsonResponse({'success': False, 'error': 'No tour_guide_email provided'})

        # שליפת הנתונים
        registrations = Registration.objects.all()

        # יצירת גוף ההודעה
        now = timezone.localtime().strftime("%d/%m/%Y %H:%M")
        body = f"דו\"ח נוכחות לסיור נכון ל-{now}:\n\n"

        for reg in registrations:
            status = "✅ נוכח" if reg.נוכחות else "❌ לא נוכח"
            body += f"{reg.שם_פרטי} {reg.שם_משפחה} | {reg.טלפון} | {status}\n"

        # שליחת מייל
        subject = f'דו"ח נוכחות לסיור - {now}'

        email_message = EmailMessage(
            subject=subject,
            body=body,
            from_email=None,  # ישתמש ב-DEFAULT_FROM_EMAIL
            to=[tour_guide_email],
        )
        email_message.send()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid method'})

from django.shortcuts import render, redirect
from .forms import TourGuideForm

def register_tour_guide(request):
    if request.method == 'POST':
        form = TourGuideForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('guide_thank_you')  # ודא שהנתיב הזה קיים
    else:
        form = TourGuideForm()
    return render(request, 'guides/tour_guide_register.html', {'form': form})


def thank_you(request):
    last_tour = Tour.objects.order_by('-id').first()
    guide_first_name = ""

    if last_tour and last_tour.שם_מדריך:
        guide_first_name = last_tour.שם_מדריך.tour_guide_first_name

    return render(request, 'guides/thank_you.html', {'tour_guide_first_name': guide_first_name})

def create_tour(request):
    if request.method == 'POST':
        form = TourForm(request.POST, request.FILES)  # ← חשוב מאוד!
        if form.is_valid():
            form.save()
            return redirect('thank_you')
    else:
        form = TourForm()
    return render(request, 'guides/create_tour.html', {'form': form})



def tour_dashboard(request):
    tours = Tour.objects.all().order_by('-תאריך', '-שעת_התחלה')
    return render(request, 'guides/tour_dashboard.html', {'tours': tours})

def edit_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = TourForm(request.POST, request.FILES, instance=tour)
        if form.is_valid():
            form.save()
            return redirect('tour_dashboard')
    else:
        form = TourForm(instance=tour)
    return render(request, 'guides/edit_tour.html', {'form': form, 'tour': tour})

def delete_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    tour.delete()
    return redirect('tour_dashboard')
from django.shortcuts import render


def tour_created(request):
    # קח את הסיור האחרון שנוצר
    last_tour = Tour.objects.order_by('-id').first()

    # אתחול שם המדריך
    guide_name = ""
    if last_tour and last_tour.שם_מדריך:
        guide_name = last_tour.שם_מדריך.tour_guide_first_name

    return render(request, 'guides/tour_created.html', {'tour_guide_first_name': guide_name})





def send_reminder_per_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    emails = [reg.אימייל for reg in tour.registrations.all() if reg.אימייל]

    messages = [
        (
            f'הזכרת השתתפות בטיול "{tour.כותרת_ראשית}"',
            f'שלום,\n\nתזכורת להשתתפותך בטיול שיתקיים בתאריך {tour.תאריך}.\n\nבברכה,\nצוות ההדרכה',
            'your@tour_guide_email.com',
            [tour_guide_email]
        )
        for tour_guide_email in emails
    ]
    send_mass_mail(messages, fail_silently=False)
    return redirect('participants_list')



def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    return render(request, 'travelers/tour_detail.html', {'tour': tour})



@csrf_exempt
def mark_present_by_code(request):
    if request.method == 'POST':
        code = request.POST.get('registration_code')
        if not code:
            return JsonResponse({'success': False, 'error': 'Missing registration code'})

        try:
            registration = Registration.objects.get(registration_code=code)
            registration.נוכחות = True
            registration.save()
            return JsonResponse({'success': True, 'id': registration.id})
        except Registration.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Registration not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

def guide_detail(request, guide_id):
    guide = get_object_or_404(TourGuide, id=guide_id)
    return render(request, 'guides/guide_detail.html', {'guide': guide})


# View to show all tour guides
from .models import TourGuide
def all_guides_view(request):
    guides = TourGuide.objects.all()
    return render(request, 'guides/all_guides.html', {'guides': guides})

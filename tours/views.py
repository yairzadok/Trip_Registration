from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Tour, Registration
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
    return render(request, 'tours/home.html', {'tours': tours})



def export_registrations_excel(request):
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="registrations.xlsx"'

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "נרשמים"

    # הוספת כותרות
    sheet.append(['שם פרטי', 'שם משפחה', 'תעודת זהות', 'טלפון', 'אימייל', 'נוכחות'])

    # הוספת הנתונים
    for registration in Registration.objects.all():
        sheet.append([
            registration.שם_פרטי,
            registration.שם_משפחה,
            registration.תעודת_זהות,
            registration.טלפון,
            registration.אימייל,
            'הגיע' if registration.נוכחות else 'לא הגיע',
        ])

    workbook.save(response)
    return response
def registration_list(request):
    tours = Tour.objects.prefetch_related('registrations').all()
    return render(request, 'tours/registration_list.html', {'tours': tours})


def register(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.סיור = tour
            registration.save()

            # יצירת QR קוד
            qr_io = generate_qr_with_text(registration.תעודת_זהות)
            qr_cid = make_msgid(domain='example.com')  # אפשר לשים דומיין אמיתי שלך

            # יצירת קישור לוויז
            location_encoded = registration.סיור.מיקום.replace(' ', '+')
            waze_link = f"https://waze.com/ul?q={location_encoded}&navigate=yes"

            # בניית תוכן המייל
            subject = 'אישור הרשמה לסיור'
            from_email = 'your_email@gmail.com'  # עדכן לאימייל שלך
            to_email = registration.אימייל

            text_content = (
                f"שלום {registration.שם_פרטי} {registration.שם_משפחה},\n"
                f"תודה שנרשמת לסיור {registration.סיור.כותרת_ראשית}!\n"
            )

            html_content = f"""
            <html lang="he" dir="rtl">
            <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
                <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <h2 style="color: #2E5C84;">שלום {registration.שם_פרטי} {registration.שם_משפחה},</h2>
                    <p>תודה שנרשמת לסיור:</p>
                    <h3 style="color: #4CAF50;">{registration.סיור.כותרת_ראשית}</h3>

                    <p><b>📅 תאריך:</b> {registration.סיור.תאריך}</p>
                    <p><b>🕘 שעה:</b> {registration.סיור.שעת_התחלה}</p>
                    <p><b>📍 מיקום:</b> {registration.סיור.מיקום}</p>

                    <div style="margin: 30px 0;">
                        <p>לנוחיותך, קוד QR לסריקה מהירה בכניסה:</p>
                        <img src="cid:{qr_cid[1:-1]}" alt="QR Code" style="max-width:200px;">
                    </div>

                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{waze_link}" style="background-color: #2196F3; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">📍 נווט עם וייז</a>
                    </div>

                    <hr style="margin: 30px 0;">

                    <p><b>👨‍🏫 מדריך הסיור:</b> {registration.סיור.שם_מדריך}</p>
                    <p><b>📞 טלפון מדריך:</b> <a href="tel:{registration.סיור.טלפון_מדריך}">{registration.סיור.טלפון_מדריך}</a></p>

                    <p style="font-size: small; color: gray; margin-top: 30px;">מייל זה נשלח אוטומטית. אין להשיב אליו.</p>
                </div>
            </body>
            </html>
            """

            # שליחת המייל
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            msg.attach_alternative(html_content, "text/html")

            # חיבור QR קוד לתוך המייל
            qr_io.seek(0)
            image = MIMEImage(qr_io.read(), _subtype="png")
            image.add_header('Content-ID', qr_cid)
            image.add_header('Content-Disposition', 'inline', filename="qr.png")
            msg.attach(image)

            msg.send()

            return render(request, 'tours/success.html', {'registration': registration})
    else:
        form = RegistrationForm()

    return render(request, 'tours/register.html', {'tour': tour, 'form': form})



def success(request):
    return render(request, 'tours/success.html')


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
    return render(request, 'tours/participants_list.html', {'registrations': registrations})


@csrf_exempt
def send_attendance_report(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if not email:
            return JsonResponse({'success': False, 'error': 'No email provided'})

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
            to=[email],
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
    return render(request, 'guides/register.html', {'form': form})


def thank_you(request):
    return render(request, 'guides/thank_you.html')

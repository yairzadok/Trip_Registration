from django.db import models  # חובה תמיד בתחילת הקובץ
import random

class TourGuide(models.Model):
    tour_guide_first_name = models.CharField("שם פרטי", max_length=100)
    tour_guide_last_name = models.CharField("שם משפחה", max_length=100)
    tour_guide_phone = models.CharField("טלפון נייד", max_length=20)
    tour_guide_email = models.EmailField("כתובת מייל")


    address = models.CharField("כתובת מגורים", max_length=255, blank=True, null=True)
    tour_guide_profile_picture = models.ImageField("תמונת פרופיל", upload_to="guide_profiles/", blank=True, null=True)
    languages = models.CharField("שפות הדרכה", max_length=255, blank=True, null=True)
    specialties = models.CharField("תחומי התמחות", max_length=255, blank=True, null=True)
    experience = models.TextField("ניסיון מקצועי", blank=True, null=True)
    recommendations = models.TextField("המלצות או קישורים", blank=True, null=True)

    def __str__(self):
        return f"{self.tour_guide_first_name} {self.tour_guide_last_name}"


class Registration(models.Model):
    סיור = models.ForeignKey("Tour", on_delete=models.CASCADE, related_name='registrations')
    שם_פרטי = models.CharField(max_length=255)
    שם_משפחה = models.CharField(max_length=255)
    registration_code = models.CharField("קוד רישום", max_length=6, blank=True, null=True)
    טלפון = models.CharField(max_length=20)
    אימייל = models.EmailField()
    נוכחות = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.registration_code:
            self.registration_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        super().save(*args, **kwargs)

class Tour(models.Model):
    כותרת_ראשית = models.CharField("כותרת ראשית", max_length=255)
    כותרת_משנית = models.CharField("כותרת משנית", max_length=255)
    תיאור = models.TextField("פרטי הטיול", blank=True, null=True)

    תאריך = models.DateField("תאריך הסיור")
    שעת_התחלה = models.TimeField("שעת התחלה")
    שעת_סיום = models.TimeField("שעת סיום משוערת", blank=True, null=True)

    מקום_המפגש = models.CharField("מקום מפגש", max_length=255)
    קישור_למפות_גוגל = models.CharField("קישור למקום בגוגל מפות", max_length=500, blank=True)

    שם_מדריך = models.ForeignKey(
        "TourGuide",
        verbose_name="שם המדריך",
        on_delete=models.CASCADE,
        related_name="tours",
        blank=True,
        null=True
    )
    טלפון_מדריך = models.CharField("טלפון מדריך", max_length=20, blank=True, null=True)

    עלות = models.DecimalField(
        "עלות הסיור",
        max_digits=8,
        decimal_places=2,
        help_text="יש להזין את העלות בשקלים חדשים (₪)",
        null=True
    )

    קהל_יעד = models.CharField(
        "קהל יעד",
        max_length=50,
        choices=[
            ("משפחות", "משפחות"),
            ("מבוגרים", "מבוגרים"),
            ("מיטבי לכת", "מיטבי לכת"),
            ("מיטיבי קשב", "מיטיבי קשב"),
        ],
        blank=True,
        null=True
    )

    רמת_קושי = models.CharField(
        "רמת קושי",
        max_length=20,
        choices=[
            ("קל", "קל"),
            ("בינוני", "בינוני"),
            ("קשה", "קשה"),
            ("קשה מאוד", "קשה מאוד"),
        ],
        blank=True,
        null=True
    )

    ציוד_נדרש = models.CharField(
        "ציוד נדרש",
        max_length=255,
        blank=True,
        null=True,
        help_text="למשל: כובע, מים, נעליים סגורות, קרם הגנה"
    )

    תמונה = models.ImageField("תמונה", upload_to='tours_images/')
    מקסימום_משתתפים = models.PositiveIntegerField("מקסימום משתתפים", default=30)

    def is_full(self):
        return self.registrations.count() >= self.מקסימום_משתתפים

    def __str__(self):
        return self.כותרת_ראשית

from django.db import models  # חובה תמיד בתחילת הקובץ

class TourGuide(models.Model):
    first_name = models.CharField("שם פרטי", max_length=100)
    last_name = models.CharField("שם משפחה", max_length=100)
    phone = models.CharField("טלפון נייד", max_length=20)
    email = models.EmailField("כתובת מייל")

    address = models.CharField("כתובת מגורים", max_length=255, blank=True, null=True)
    license_file = models.FileField("קובץ רישיון הדרכה", upload_to='licenses/', blank=True, null=True)
    license_number = models.CharField("מספר רישיון", max_length=100, blank=True, null=True)
    languages = models.CharField("שפות הדרכה", max_length=255, blank=True, null=True)
    specialties = models.CharField("תחומי התמחות", max_length=255, blank=True, null=True)
    experience = models.TextField("ניסיון מקצועי", blank=True, null=True)
    recommendations = models.TextField("המלצות או קישורים", blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Tour(models.Model):
    כותרת_ראשית = models.CharField(max_length=255)
    כותרת_משנית = models.CharField(max_length=255)
    תאריך = models.DateField()
    מיקום_ידני = models.CharField(max_length=500, blank=True)
    מיקום = models.CharField(max_length=255)
    שעת_התחלה = models.TimeField()
    שם_מדריך = models.ForeignKey("TourGuide", on_delete=models.CASCADE, related_name="tours", blank=True, null=True)
    תמונה = models.ImageField(upload_to='tours_images/')
    טלפון_מדריך = models.CharField(max_length=20, blank=True, null=True)
    עלות = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="עלות הסיור",
        help_text="יש להזין את העלות בשקלים חדשים (₪)",
        null=True
    )

    def __str__(self):
        return self.כותרת_ראשית

class Registration(models.Model):
    סיור = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='registrations')
    שם_פרטי = models.CharField(max_length=255)
    שם_משפחה = models.CharField(max_length=255)
    תעודת_זהות = models.CharField(max_length=20, unique=True)
    טלפון = models.CharField(max_length=20)
    אימייל = models.EmailField()
    נוכחות = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.שם_פרטי} {self.שם_משפחה} ({self.סיור.כותרת_ראשית})"

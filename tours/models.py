from django.db import models  # זה חובה בתחילת הקובץ!

class Tour(models.Model):
    כותרת_ראשית = models.CharField(max_length=255)
    כותרת_משנית = models.CharField(max_length=255)
    תאריך = models.DateField()
    מיקום_ידני = models.CharField(max_length=500, blank=True)
    מיקום = models.CharField(max_length=255)
    שעת_התחלה = models.TimeField()
    שם_מדריך = models.CharField(max_length=255)
    תמונה = models.ImageField(upload_to='tours_images/')
    טלפון_מדריך = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.כותרת_ראשית

class Registration(models.Model):
    סיור = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='registrations')
    שם_פרטי = models.CharField(max_length=255)
    שם_משפחה = models.CharField(max_length=255)
    תעודת_זהות = models.CharField(max_length=20, unique=True)  # מוודאים שלא ירשמו פעמיים
    טלפון = models.CharField(max_length=20)
    אימייל = models.EmailField()
    נוכחות = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.שם_פרטי} {self.שם_משפחה} ({self.סיור.כותרת_ראשית})"

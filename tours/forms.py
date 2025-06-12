from django import forms
from .models import Registration, TourGuide
from .models import Tour

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['שם_פרטי', 'שם_משפחה', 'טלפון', 'אימייל']
        labels = {
            'שם_פרטי': 'שם פרטי',
            'שם_משפחה': 'שם משפחה',
             'טלפון': 'טלפון',
            'אימייל': 'אימייל',
        }
        widgets = {
            'שם_פרטי': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'הכנס שם פרטי'}),
            'שם_משפחה': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'הכנס שם משפחה'}),
            'טלפון': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '050-1234567'}),
            'אימייל': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'name@example.com',
                'maxlength': '254',
                'pattern': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$',
                'title': 'אנא הזן כתובת אימייל תקינה'
            }),
        }

class TourGuideForm(forms.ModelForm):
    class Meta:
        model = TourGuide
        fields = '__all__'
        widgets = {
            'tour_guide_first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'tour_guide_last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'tour_guide_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'tour_guide_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'license_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'languages': forms.TextInput(attrs={'class': 'form-control'}),
            'specialties': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'recommendations': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = '__all__'
        widgets = {
            'כותרת_ראשית': forms.TextInput(attrs={'class': 'form-control'}),
            'כותרת_משנית': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'תאריך': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'מיקום_ידני': forms.TextInput(attrs={'class': 'form-control'}),
            'מיקום': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'קישור למיקום במפה (למשל Google Maps)'
            }),
            'שעת_התחלה': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'שם_מדריך': forms.Select(attrs={'class': 'form-select'}),
            'תמונה': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'טלפון_מדריך': forms.TextInput(attrs={'class': 'form-control'}),
            'עלות': forms.NumberInput(attrs={'class': 'form-control'}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['שם_מדריך'].queryset = TourGuide.objects.all()
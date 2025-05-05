from django import forms
from .models import Registration, TourGuide

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['שם_פרטי', 'שם_משפחה', 'תעודת_זהות', 'טלפון', 'אימייל']
        labels = {
            'שם_פרטי': 'שם פרטי',
            'שם_משפחה': 'שם משפחה',
            'תעודת_זהות': 'תעודת זהות',
            'טלפון': 'טלפון',
            'אימייל': 'אימייל',
        }
        widgets = {
            'שם_פרטי': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'הכנס שם פרטי'}),
            'שם_משפחה': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'הכנס שם משפחה'}),
            'תעודת_זהות': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '9 ספרות',
                'pattern': '\\d*',
                'inputmode': 'numeric',
                'maxlength': '9',
                'title': 'יש להזין ספרות בלבד'
            }),
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
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'license_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'languages': forms.TextInput(attrs={'class': 'form-control'}),
            'specialties': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'recommendations': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

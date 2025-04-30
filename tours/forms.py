from django import forms
from .models import Registration

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

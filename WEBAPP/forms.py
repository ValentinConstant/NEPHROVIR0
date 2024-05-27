from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import CustomUser

CustomUser = get_user_model()

from .models import Patient

from .models import Test, LotDeTest

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        exclude = ['user', 'patient', 'gen1', 'bio1', 'immuno1', 'distance_svm', 'indice_knn', 'risque']
        widgets = {
            'test_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        serial_number = cleaned_data.get('serial_number')
        date_test = cleaned_data.get('test_date')

        # Vérification que le numéro de série du lot existe dans la table de lot
        if not LotDeTest.objects.filter(numero_lot=serial_number).exists():
            self.add_error('serial_number', "Le numéro de série de lot n'existe pas.")

        # Vérification que la date du test est antérieure à la date de péremption du lot
        if LotDeTest.objects.filter(numero_lot=serial_number).exists():
            lot = LotDeTest.objects.get(numero_lot=serial_number)
            if date_test >= lot.date_peremption:
                self.add_error('test_date', "La date du test doit être antérieure à la date de péremption du lot.")

        return cleaned_data

        
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ['user']  # Exclure le champ utilisateur
        fields = ['patient_id', 'sex', 'birth_date', 'hospital']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'sex': forms.Select(),
        }   

    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        self.fields['sex'].initial = 'F'
        self.fields['sex'].empty_label = "Sélectionner le sexe"
        self.fields['sex'].required = True

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "center")

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Cette adresse email est déjà utilisée.")
        return username


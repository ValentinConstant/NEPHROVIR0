from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .forms import PatientForm
from .models import Patient

from .forms import TestForm
from .models import Patient, Test


from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .models import Test


# Importez joblib pour charger le modèle
from joblib import load
from django.conf import settings
import os

from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def calcul_age(date_naissance):
    # Obtenir la date d'aujourd'hui
    date_aujourdhui = datetime.now().date()

    # Calculer l'âge en années
    age = date_aujourdhui.year - date_naissance.year - ((date_aujourdhui.month, date_aujourdhui.day) < (date_naissance.month, date_naissance.day))

    return age


from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont



def generate_png(request,test_id):
    # Créer un objet StringIO pour stocker le PDF en mémoire
    buffer = BytesIO()

    test = get_object_or_404(Test, id=test_id, user=request.user)

    # Créer un objet Canvas de ReportLab
    p = canvas.Canvas(buffer, pagesize=letter)

    # Calcul de la hauteur pour que le logo occupe 1/8 de la hauteur de la page A4
    logo_height = 842 
    logo_width = 595  # Prendre toute la largeur de la page A4

    # Position du logo pour qu'il soit en haut de la page
    template_path = settings.STATIC_ROOT + '/WEBAPP/template.png'

    output_path = settings.STATIC_ROOT + '/WEBAPP/output_image.png'

    # Charger l'image template
    template_image = Image.open(template_path)
    draw = ImageDraw.Draw(template_image)
    
    font_size = 20
    font = ImageFont.truetype(font_size)
    # Position du texte
    text_position = (330, 711)  # Coordonnées (x, y) pour placer le texte

    # Ajouter le texte à l'image
    draw.text(text_position, f"{test.serial_number}", font=font, fill="black")

    # Enregistrer l'image modifiée
    template_image.save(output_path)

    return template_image



def download_test_pdf(request, test_id):

    test = get_object_or_404(Test, id=test_id, user=request.user)




    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="test_{}.pdf"'.format(test.id)

    p = canvas.Canvas(response, pagesize=A4)

    # Calcul de la hauteur pour que le logo occupe 1/8 de la hauteur de la page A4
    logo_height = 842 
    logo_width = 595  # Prendre toute la largeur de la page A4

    # Position du logo pour qu'il soit en haut de la page
    logo_path = settings.STATIC_ROOT + '/WEBAPP/template.png'
    p.drawImage(logo_path, 0, 0, width=logo_width, height=logo_height, preserveAspectRatio=True, anchor='c')



   # Définition de la police et de la taille de police
    p.setFont("Helvetica-Bold", 12)

    p.drawString(330, 711, f"{test.serial_number}")
    p.drawString(130, 589, f"{test.patient.birth_date}")
    p.drawString(130, 560, f"{test.patient.sex}")
    age_patient = calcul_age(test.patient.birth_date)
    p.drawString(130, 530, f"{age_patient}")

    # Définition de la police et de la taille de police
    p.setFont("Helvetica", 8)

    p.drawString(468, 603, f"{test.BKv_peptide_activation}%")
    p.drawString(445, 592, f"{test.background}%")
    p.drawString(430, 582, f"{test.bio_sample_date}")



    p.drawString(450, 561, f"{test.BK_viral_load}")
    p.drawString(430, 550, f"{test.immuno_sample_date}")



    p.drawString(460, 528, f"{test.mismatch_number}")
    p.drawString(430, 518, f"{test.gen_sample_date}")

   # Définition de la police et de la taille de police
    p.setFont("Helvetica-Bold", 14)
    p.drawString(40, 305, f"{ round(test.distance_svm * 10) / 10}")

    p.showPage()
    p.save()

    return response




@login_required
def add_test(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.user = request.user
            test.patient = patient
            calculate_and_save_test(test)  
            return render(request, 'WEBAPP/read_test.html', {'test': test})  
    else:
        form = TestForm()
    return render(request, 'WEBAPP/add_test.html', {'form': form, 'patient': patient})

def calculate_and_save_test(test):
    test.bio1 = calculate_bio1(test.BKv_peptide_activation,test.background)
    test.gen1 = calculate_gen1(test.mismatch_number)
    test.immuno1 = calculate_immuno1(test.BK_viral_load, test.power_field)
    test.distance_svm = calculate_distance_svm(test.gen1, test.bio1, test.immuno1)
    test.indice_knn = calculate_indice_knn(test.gen1, test.bio1, test.immuno1)
    test.risque = calculate_risque(test.immuno1)
    test.save()

@login_required
def edit_test(request, test_id):
    test = get_object_or_404(Test, id=test_id, user=request.user)
    if request.method == 'POST':
        form = TestForm(request.POST, instance=test)
        if form.is_valid():
            updated_test = form.save(commit=False)
            calculate_and_save_test(updated_test)
            return render(request, 'WEBAPP/read_test.html', {'test': updated_test})  
    else:
        form = TestForm(instance=test)
    return render(request, 'WEBAPP/edit_test.html', {'form': form, 'test': test})

@login_required
def delete_test(request, test_id):
    test = get_object_or_404(Test, id=test_id, user=request.user)
    if request.method == 'POST':
        test.delete()
        return redirect('welcome')
    return render(request, 'WEBAPP/delete_test_confirm.html', {'test': test})

@login_required
def read_test(request, test_id):
    test = get_object_or_404(Test, id=test_id, user=request.user)
    return render(request, 'WEBAPP/read_test.html', {'test': test})

def calculate_bio1(BKv_peptide_activation,background):
    import math
    value = BKv_peptide_activation - background
    value = value * 10000
    value = math.log10(value)
    return value


def calculate_gen1(mismatch_number):
    return mismatch_number

def calculate_immuno1(BK_viral_load,power_field):
    value = BK_viral_load
    return value

def calculate_distance_svm(gen1, bio1, immuno1):
 
    try:# Chemin où votre modèle est stocké
        model_path = os.path.join(settings.BASE_DIR, 'WEBAPP/resources', 'svm_model.joblib')
        # Charger le modèle SVM pré-entraîné
        loaded_model = load(model_path)
    
        # Créer un vecteur à partir des entrées
        point = [gen1, bio1, immuno1]
    
    # Calculer la distance à la frontière de décision
        distance = loaded_model.decision_function([point])
        return distance[0]
    except FileNotFoundError:
        raise Exception("Le modèle SVM n'a pas été trouvé à l'emplacement spécifié.")


def calculate_indice_knn(gen1, bio1, immuno1):
    return int((gen1 + bio1 + immuno1) / 3)  # Exemple simpliste

def calculate_risque(immuno1):
    return "Élevé" if immuno1 > 5 else "Faible"


@login_required
def read_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id, user=request.user)  # Assurez-vous que seul l'utilisateur qui a créé le patient peut voir les détails
    return render(request, 'WEBAPP/read_patient.html', {'patient': patient})

@login_required
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user  # Assigner l'utilisateur connecté
            patient.save()
            return redirect('welcome')
    else:
        form = PatientForm()
    return render(request, 'WEBAPP/add_patient.html', {'form': form})

from django.shortcuts import render, redirect
from .forms import PatientForm, TestForm


# views.py
from django.shortcuts import render, redirect
from .models import Patient, Test
from .forms import PatientForm, TestForm


@login_required
def add_patient_and_test(request):
    if request.method == 'POST':
        patient_form = PatientForm(request.POST)
        test_form = TestForm(request.POST)
        if patient_form.is_valid() and test_form.is_valid():
            patient = patient_form.save(commit=False)
            patient.user = request.user  # Assign the logged-in user to the patient
            patient.save()
            
            test = test_form.save(commit=False)
            test.user = request.user  # Assign the logged-in user to the test
            test.patient = patient
            calculate_and_save_test(test)  
            
            messages.success(request, 'Patient and test information added successfully.')
            return redirect('welcome')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        patient_form = PatientForm()
        test_form = TestForm()
    
    return render(request, 'WEBAPP/add_patient_and_test.html', {'patient_form': patient_form, 'test_form': test_form})

@login_required
def welcome(request):
    patients = request.user.patients.all()  # Afficher uniquement les patients de l'utilisateur connecté
    return render(request, 'WEBAPP/welcome.html', {'patients': patients})

def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)  # S'assurer que l'utilisateur est passé en tant qu'argument
                return redirect('welcome')
        else:
            messages.error(request, 'Identifiants invalides/Compte Inactivé.')
            return redirect('custom_login')
    return render(request, 'WEBAPP/login.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                form.add_error('username', 'Cette adresse email est déjà utilisée.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'WEBAPP/register.html', {'form': form})

def home(request):
    return render(request, 'WEBAPP/home.html')


@login_required
def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id, user=request.user)  # S'assurer que le patient appartient à l'utilisateur
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, "Les informations du patient ont été mises à jour.")
            return redirect('welcome')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'WEBAPP/edit_patient.html', {'form': form})        

@login_required
def delete_patient_confirm(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id, user=request.user)
    if request.method == 'POST':
        patient.delete()
        messages.success(request, "Le patient a été supprimé.")
        return redirect('welcome')
    return render(request, 'WEBAPP/delete_patient_confirm.html', {'patient': patient})   

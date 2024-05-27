from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager

from django.conf import settings
from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator
import datetime

class LotDeTest(models.Model):
    numero_lot = models.CharField(
        max_length=4,
        validators=[
            MaxLengthValidator(4),
            MinLengthValidator(4),
            RegexValidator(r'^[0-9]*$', message="Le numéro de lot doit être composé uniquement de chiffres.")
        ],
        unique=True
    )
    date_peremption = models.DateField()
    date_ajout = models.DateTimeField(auto_now_add=True)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.numero_lot

class Test(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tests')
    patient = models.ForeignKey("Patient", related_name='tests', on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=4)
    test_date = models.DateField()

    bio_sample_date = models.DateField(default=datetime.date.today)
    BKv_peptide_activation = models.IntegerField(max_length=3,default='0')
    background = models.IntegerField(max_length=3,default='0')
   
    immuno_sample_date = models.DateField(default=datetime.date.today)
    BK_viral_load = models.IntegerField(default='1')
    POWER_CHOICES = [
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
    ]
    power_field = models.IntegerField(choices=POWER_CHOICES,default='4')
 
    gen_sample_date = models.DateField(default=datetime.date.today)
    mismatch_number_CHOICES = [
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
        (11, '11'),
        (12, '12'),
    ]
    mismatch_number = models.IntegerField(choices=mismatch_number_CHOICES,default='4')
 
    gen1 = models.FloatField(null=True, blank=True)
    bio1 = models.FloatField(null=True, blank=True)
    immuno1 = models.FloatField(null=True, blank=True)

    distance_svm = models.FloatField(null=True, blank=True)
    indice_knn = models.IntegerField(null=True, blank=True)
    risque = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.serial_number} - {self.test_date}"



class Patient(models.Model):
    SEX_CHOICES = (
        ('M', 'Homme'),
        ('F', 'Femme'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patients', verbose_name="Utilisateur")
    patient_id = models.CharField(max_length=100, verbose_name="Identifiant du Patient")
    sex = models.CharField(max_length=1, choices=(('M', 'Homme'), ('F', 'Femme')), verbose_name="Sexe")
    birth_date = models.DateField(verbose_name="Date de naissance")
    hospital = models.CharField(max_length=100, verbose_name="Hôpital")

    def __str__(self):
        return self.patient_id




    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Crée et sauvegarde un utilisateur avec l'email donné et le mot de passe."""
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = False  # Définir is_active à False
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    #username = None  # On retire le champ username
    username = models.EmailField('email address', unique=True)  # Email comme identifiant unique
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=150, blank=True)
    center = models.CharField('center', max_length=100, blank=True)
    #is_validated = models.BooleanField('is validated', default=False)
    is_active = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

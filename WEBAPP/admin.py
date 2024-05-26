from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Patient
from .models import Test
from .models import LotDeTest

class TestAdmin(admin.ModelAdmin):
    list_display = ['serial_number', 'test_date']

admin.site.register(Test, TestAdmin)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Mettre à jour l'ordre de tri pour utiliser 'email' au lieu de 'username'
    #ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'center')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}
        ),
    )
    list_display = ('username', 'first_name', 'last_name', 'center', 'is_active', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'center')
    list_filter = ('center', 'is_active', 'is_staff')

admin.site.register(CustomUser, CustomUserAdmin)


class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'user', 'sex', 'birth_date', 'hospital')
    list_filter = ('user', 'sex', 'hospital')
    search_fields = ('patient_id', 'hospital')

admin.site.register(Patient, PatientAdmin)


class LotDeTestAdmin(admin.ModelAdmin):
    list_display = ['numero_lot', 'date_peremption', 'date_ajout', 'admin']
    list_filter = ['date_peremption', 'date_ajout']
    search_fields = ['numero_lot', 'admin__email']

admin.site.register(LotDeTest, LotDeTestAdmin)
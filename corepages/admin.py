
from django.contrib import admin
from .models import CorePage
from django import forms
from ckeditor.widgets import CKEditorWidget

class CorePageAdminForm(forms.ModelForm):
	content = forms.CharField(widget=CKEditorWidget())
	class Meta:
		model = CorePage
		fields = '__all__'

@admin.register(CorePage)
class CorePageAdmin(admin.ModelAdmin):
	form = CorePageAdminForm
	list_display = ('page', 'title')

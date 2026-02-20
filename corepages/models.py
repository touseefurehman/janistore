
from django.db import models
from ckeditor.fields import RichTextField

class CorePage(models.Model):
	PAGE_CHOICES = [
		('about', 'About Us'),
		('privacy', 'Privacy Policy'),
		('terms', 'Terms & Conditions'),
		('contact', 'Contact Us'),
	]
	page = models.CharField(max_length=20, choices=PAGE_CHOICES, unique=True)
	title = models.CharField(max_length=100)
	content = RichTextField()

	def __str__(self):
		return self.get_page_display()

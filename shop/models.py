from django.db import models
from django.urls import reverse

class Category(models.Model):
	name = models.CharField(max_length=100)
	slug = models.SlugField(unique=True)
	image = models.ImageField(upload_to='categories/', blank=True, null=True)
	image_link = models.URLField(blank=True, null=True, help_text="Optional external image URL.")

	class Meta:
		verbose_name_plural = 'Categories'

	def __str__(self):
		return self.name


class Product(models.Model):
	name = models.CharField(max_length=200)
	slug = models.SlugField(unique=True)
	category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
	image = models.ImageField(upload_to='products/')
	image_link = models.URLField(blank=True, null=True, help_text="Optional external image URL.")
	price = models.DecimalField(max_digits=10, decimal_places=2)
	old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	short_description = models.CharField(max_length=255)
	description = models.TextField()
	is_featured = models.BooleanField(default=False)
	is_flash_sale = models.BooleanField(default=False, help_text="Show in Flash Sales section")
	is_best_selling = models.BooleanField(default=False, help_text="Show in Best Selling Products section")
	is_new_arrival = models.BooleanField(default=False, help_text="Show in New Arrival section")
	is_explore = models.BooleanField(default=False, help_text="Show in Explore Our Products section")
	seo_title = models.CharField(max_length=255, blank=True)
	seo_description = models.CharField(max_length=255, blank=True)
	related_products = models.ManyToManyField('self', blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def get_absolute_url(self):
		return reverse('product_detail', args=[str(self.id)])

	def __str__(self):
		return self.name


class Cart(models.Model):
	session_key = models.CharField(max_length=40)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Cart {self.id}"


# Restore CartItem model
class CartItem(models.Model):
	cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)

	def __str__(self):
		return f"{self.quantity} x {self.product.name}"


# Product Review Model
from django.contrib.auth.models import User

class ProductReview(models.Model):
	product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
	comment = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Review by {self.user.username} on {self.product.name}"

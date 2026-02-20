

from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Product, Category, Cart, CartItem, ProductReview
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Product, Category
@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
	list_display = ("product", "user", "rating", "created_at")
	search_fields = ("product__name", "user__username", "comment")
	list_filter = ("rating", "created_at")


class CategoryResource(resources.ModelResource):
	class Meta:
		model = Category

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
	resource_class = CategoryResource
	prepopulated_fields = {"slug": ("name",)}
	list_display = ("name", "slug", "image", "image_link")
	fields = ("name", "slug", "image", "image_link")

class ProductResource(resources.ModelResource):
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(Category, 'slug')  # ✅ match by slug
    )

    class Meta:
        model = Product

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
	resource_class = ProductResource
	prepopulated_fields = {"slug": ("name",)}
	list_display = (
		"name", "category", "price", "is_featured", "is_flash_sale", "is_best_selling", "is_new_arrival", "is_explore", "image_link"
	)
	search_fields = ("name", "category__name")
	list_filter = ("category", "is_featured", "is_flash_sale", "is_best_selling", "is_new_arrival", "is_explore")
	filter_horizontal = ("related_products",)
	fieldsets = (
		(None, {"fields": ("name", "slug", "category", "image", "image_link", "price", "old_price", "short_description", "description",
						  "is_featured", "is_flash_sale", "is_best_selling", "is_new_arrival", "is_explore")}),
		("SEO", {"fields": ("seo_title", "seo_description")}),
		("Related", {"fields": ("related_products",)}),
	)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
	list_display = ("id", "session_key", "created_at")

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
	list_display = ("cart", "product", "quantity")

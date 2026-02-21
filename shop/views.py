from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
def signup_view(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		email = request.POST.get('email')
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		if password1 != password2:
			messages.error(request, 'Passwords do not match.')
		elif User.objects.filter(username=username).exists():
			messages.error(request, 'Username already exists.')
		elif User.objects.filter(email=email).exists():
			messages.error(request, 'Email already exists.')
		else:
			user = User.objects.create_user(username=username, email=email, password=password1)
			messages.success(request, 'Account created successfully. Please log in.')
			return redirect('home')
	return render(request, 'signup.html')

from django.shortcuts import render
from .models import Product, Category, Cart
from django.core.paginator import Paginator

def home(request):
	hero_products = Product.objects.filter(is_featured=True)[:5]
	flash_sale_products = Product.objects.filter(is_flash_sale=True)[:10]
	best_selling_products = Product.objects.filter(is_best_selling=True)[:8]
	new_arrival_products = Product.objects.filter(is_new_arrival=True)[:8]
	explore_products = Product.objects.filter(is_explore=True)[:8]
	categories = Category.objects.all()
	return render(request, 'home.html', {
		'hero_products': hero_products,
		'featured_products': flash_sale_products,
		'categories': categories,
		'best_selling_products': best_selling_products,
		'explore_products': explore_products,
		'new_arrival_products': new_arrival_products,
	})

def product_list(request):
    query = request.GET.get('q', '').strip()
    page_number = request.GET.get('page', 1)
    
   
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    
   
    paginator = Paginator(products, 12)  
    
    
    page_obj = paginator.get_page(page_number)
	
    
    return render(request, 'product_list.html', {'page_obj': page_obj, 'query': query})

from .models import ProductReview
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

def product_detail(request, pk):
	product = get_object_or_404(Product, pk=pk)
	related = product.related_products.all()
	reviews = product.reviews.select_related('user').order_by('-created_at')

	if request.method == 'POST' and request.POST.get('review_submit'):
		if request.user.is_authenticated:
			rating = int(request.POST.get('rating', 5))
			comment = request.POST.get('comment', '').strip()
			if comment:
				ProductReview.objects.create(
					product=product,
					user=request.user,
					rating=rating,
					comment=comment
				)
				return HttpResponseRedirect(reverse('product_detail', args=[product.pk]))

	return render(request, 'product_detail.html', {
		'product': product,
		'related': related,
		'reviews': reviews,
	})

def cart_view(request):
	session_key = request.session.session_key or request.session.create()
	cart, _ = Cart.objects.get_or_create(session_key=session_key)
	return render(request, 'cart.html', {'cart': cart})

def category_view(request, slug):
	category = Category.objects.get(slug=slug)
	products = category.products.all()
	paginator = Paginator(products, 12)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request, 'category.html', {'category': category, 'products': page_obj, 'page_obj': page_obj})

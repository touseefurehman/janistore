

from django.shortcuts import render, get_object_or_404
from .models import CorePage

def corepage_view(request, page):
    corepage = get_object_or_404(CorePage, page=page)
    return render(request, f'corepages/{page}.html', {'corepage': corepage})

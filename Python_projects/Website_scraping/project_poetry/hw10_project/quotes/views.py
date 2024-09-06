from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .forms import QuoteForm, AuthorForm
from .models import Author, Quote

# Create your views here.

def main(request, page=1):
    quotes = Quote.objects.select_related('author').prefetch_related('tags').all()
    per_page = 10
    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.page(page)

    return render(request, "quotes/index.html", context={"quotes": quotes_on_page, "paginator":paginator})

@login_required()
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.user = request.user
            quote.save()
            form.save_m2m()
            return redirect('quotes:root')
    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form})

def author_detail(request, fullname):
    author = get_object_or_404(Author, fullname=fullname)
    return render(request, 'quotes/author_detail.html', {'author': author})

@login_required()
def author_create(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes:add_quote')
    else:
        form = AuthorForm()
    return render(request, 'quotes/author_create.html', {'form': form})


from .forms import TagForm, AuthorForm, QuoteForm
from .models import Tag, Author, Quote
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


def main(request):
    quotes = Quote.objects.all()
    return render(request, 'quoteapp/index.html', {"quotes": quotes})


@login_required
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/tag.html', {'form': form})

    return render(request, 'quoteapp/tag.html', {'form': TagForm()})


@login_required
def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save(commit=False)
            author.user = request.user
            author.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/author.html', {'form': form})

    return render(request, 'quoteapp/author.html', {'form': AuthorForm()})


def author_detail(request, author_name):
    author = get_object_or_404(Author, fullname=author_name)
    return render(request, 'quoteapp/author_detail.html', {'author': author})


@login_required
def quote(request):

    tags = Tag.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.user = request.user
            new_quote.save()

            choice_tags = Tag.objects.filter(
                name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/quote.html', {"tags": tags, 'form': form})
    return render(request, 'quoteapp/quote.html', {"tags": tags, 'form': QuoteForm()})


def detail(request,  quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)
    return render(request, 'quoteapp/detail.html', {"quote": quote})


@login_required
def delete_quote(request, quote_id):
    Quote.objects.get(pk=quote_id, user=request.user).delete()
    return redirect(to='quoteapp:main')

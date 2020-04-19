from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm

# Create your views here.
def index(request):
    reviews = Review.objects.order_by('-pk')
    ranks = Review.objects.raw('select rowid as id, movie_title, avg_rate from (select movie_title, avg(rank) as avg_rate from community_review group by movie_title order by avg_rate desc) LIMIT 3')
    context = {
        'reviews':reviews,
        'ranks': ranks,
    }
    return render(request, 'community/review_list.html', context)

@login_required(redirect_field_name='')
def create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('community:index')
    else:
        form = ReviewForm()
    context = {
        'form': form
    }
    return render(request, 'community/form.html', context)

def detail(request, pk):
    review = get_object_or_404(Review, id=pk)
    context = {
        'review': review
    }
    return render(request, 'community/review_detail.html', context)

@login_required
def update(request, pk):
    review = get_object_or_404(Review, id=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review =form.save()
            return redirect('community:detail', review.pk)
    else:
        form = ReviewForm(instance=review)
    context = {
        'form':form
    }
    return render(request, 'community/form.html', context)

@login_required
@require_POST
def delete(request, pk):
    review = get_object_or_404(Review, id=pk)
    review.delete()
    return redirect('community:index')

# 영화 제목으로 검색!
def search(request):
    keyword = request.POST.get('keyword')
    reviews = Review.objects.filter(movie_title__icontains=keyword)
    context = {
        'reviews': reviews,
        'keyword': keyword,
    }
    return render(request, 'community/review_list.html', context)
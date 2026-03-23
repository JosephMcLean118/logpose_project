from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from logpose.models import Review, UserProfile
from logpose.forms import ReviewForm

# Create your views here.

def index(request):
    return render(request, 'logpose/base.html')

def review_detail(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    profile = UserProfile.objects.filter(user=review.user).first()

    context = {
        'review': review,
        'profile': profile,
    }
    return render(request, 'logpose/review_detail.html', context)


def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = User.objects.first()
            review.save()
            return redirect('logpose:review_detail', review_id=review.id)
    else:
        form = ReviewForm()

    return render(request, 'logpose/create_review.html', {'form': form})

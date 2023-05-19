from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Diary
from .forms import DiaryForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .sentiment_classification import sentiment_classify
from .sentiment_analysis import sentiment_analyse


@login_required(login_url='common:login')
def index(request):
    page = request.GET.get('page', '1')
    diary_list = Diary.objects.filter(author=request.user).order_by('-create_date')
    paginator = Paginator(diary_list, 10)
    page_obj = paginator.get_page(page)
    weekly_result, monthly_result = sentiment_analyse(diary_list)
    context = {'diary_list': page_obj,
               "weekly_happy": weekly_result["happy"],
               "weekly_sad": weekly_result["sad"],
               "weekly_angry": weekly_result["angry"],
               "monthly_happy": monthly_result["happy"],
               "monthly_sad": monthly_result["sad"],
               "monthly_angry": monthly_result["angry"],
               }
    return render(request, 'diary/diary_list.html', context)


@login_required(login_url='common:login')
def diary_create(request):
    if request.method == 'POST':
        form = DiaryForm(request.POST)
        if form.is_valid():
            diary = form.save(commit=False)
            diary.author = request.user
            diary.create_date = timezone.now()
            diary.sentiment = sentiment_classify(form.cleaned_data['content'])
            diary.save()
            return redirect('diary:index')
    else:
        form = DiaryForm()
    context = {'form': form}
    return render(request, 'diary/diary_form.html', context)

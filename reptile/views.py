from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Reptile, FeedingRecord
from .forms import FeedingRecordForm, ReptileForm
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
import json


# ========================
# 基本ページ
# ========================

def home(request):
    return render(request, 'home.html')


@login_required
def index(request):
    return render(request, "calender.html")


# ========================
# 認証系
# ========================

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "アカウント作成成功！ログインしてください")
            return redirect('login')
        else:
            messages.error(request, f"エラー: {form.errors}")
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('calender')
        else:
            messages.error(request, "ログイン失敗")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ========================
# 爬虫類管理
# ========================

@login_required
def reptile_list(request):
    reptiles = Reptile.objects.filter(owner=request.user)
    return render(request, 'reptile_list.html', {'reptiles': reptiles})


@login_required
def reptile_detail(request, id):
    reptile = get_object_or_404(Reptile, pk=id, owner=request.user)
    return render(request, 'reptile_detail.html', {'reptile': reptile})


@login_required
def reptile_profile(request, reptile_id):
    reptile = get_object_or_404(Reptile, id=reptile_id, owner=request.user)
    feeding_records = FeedingRecord.objects.filter(reptile=reptile).order_by('-date')

    return render(request, 'reptile_profile.html', {
        'reptile': reptile,
        'feeding_records': feeding_records,
    })


@login_required
def add_reptile(request):
    if request.method == 'POST':
        form = ReptileForm(request.POST, request.FILES)
        if form.is_valid():
            reptile = form.save(commit=False)
            reptile.owner = request.user
            reptile.save()
            return redirect('reptile_list')
    else:
        form = ReptileForm()

    return render(request, 'add_reptile.html', {'form': form})


@login_required
def edit_reptile_profile(request, reptile_id):
    reptile = get_object_or_404(Reptile, id=reptile_id, owner=request.user)

    if request.method == 'POST':
        form = ReptileForm(request.POST, request.FILES, instance=reptile)
        if form.is_valid():
            form.save()
            return redirect('reptile_profile', reptile_id=reptile.id)
    else:
        form = ReptileForm(instance=reptile)

    return render(request, 'edit_reptile_profile.html', {
        'form': form,
        'reptile': reptile
    })


# ========================
# 餌やり記録
# ========================

@login_required
def create_feeding_record(request):
    reptiles = Reptile.objects.filter(owner=request.user)

    if request.method == 'POST':
        form = FeedingRecordForm(request.POST, request.FILES)

        if form.is_valid():
            feeding_record = form.save(commit=False)

            reptile = get_object_or_404(
                Reptile,
                id=form.cleaned_data['reptile'].id,
                owner=request.user
            )

            feeding_record.reptile = reptile

            try:
                feeding_record.save()

                # 体重更新
                if feeding_record.weight:
                    reptile.weight = feeding_record.weight
                    reptile.save()

                messages.success(request, "記録保存完了！")
                return redirect('calender')

            except Exception as e:
                messages.error(request, f"保存エラー: {e}")
        else:
            messages.error(request, f"フォームエラー: {form.errors}")

    else:
        form = FeedingRecordForm()

    return render(request, 'feeding_list.html', {
        'form': form,
        'reptiles': reptiles
    })


@login_required
def feeding_logs_api(request):
    records = FeedingRecord.objects.filter(
        reptile__owner=request.user
    ).values(
        'date', 'food_type', 'health_status',
        'memo', 'reptile__name',
        'feces_and_urine', 'care_items', 'shedding', 'weight'
    )

    events = []

    for r in records:
        events.append({
            'title': f"{r['reptile__name']} 餌",
            'start': r['date'].isoformat(),
            'description': f"{r['memo']}\n体重:{r['weight']}",
            'color': '#32CD32'
        })

    return JsonResponse(events, safe=False)


# ========================
# カレンダー
# ========================

@login_required
def calender_view(request):
    records = FeedingRecord.objects.filter(reptile__owner=request.user)

    events = [
        {
            'title': r.reptile.name,
            'start': r.date.isoformat(),
            'extendedProps': {
                'description': r.memo
            }
        }
        for r in records
    ]

    reptiles = Reptile.objects.filter(owner=request.user)

    return render(request, 'calender.html', {
        'events': json.dumps(events),
        'reptiles': reptiles
    })


# ========================
# 体重グラフ
# ========================

@login_required
def weight_history(request, reptile_id):
    reptile = get_object_or_404(Reptile, id=reptile_id, owner=request.user)

    records = FeedingRecord.objects.filter(reptile=reptile).order_by('date')

    dates = []
    weights = []

    for r in records:
        if r.weight:
            dates.append(r.date.strftime('%Y-%m-%d'))
            weights.append(float(r.weight))

    reptiles = Reptile.objects.filter(owner=request.user)

    return render(request, 'weight_history.html', {
        'reptile': reptile,
        'reptiles': reptiles,
        'dates': json.dumps(dates),
        'weights': json.dumps(weights),
    })


# ========================
# 統計
# ========================

@login_required
def feeding_record_count(request):
    data = FeedingRecord.objects.filter(
        reptile__owner=request.user
    ).annotate(month=TruncMonth('date')) \
     .values('month') \
     .annotate(count=Count('id')) \
     .order_by('month')

    months = [d['month'].strftime('%Y-%m') for d in data]
    counts = [d['count'] for d in data]

    return JsonResponse({
        'months': months,
        'counts': counts
    })

def feeding_record_list(request):
    month = request.GET.get('month')
    reptile_id = request.GET.get('reptile_id')

    records = FeedingRecord.objects.all()
    if month:
        records = records.filter(date__month=month)
    if reptile_id:
        records = records.filter(reptile_id=reptile_id)

    reptiles = Reptile.objects.all()
    return render(request, 'feeding_record_list.html', {
        'feeding_records': records,
        'reptiles': reptiles
    })
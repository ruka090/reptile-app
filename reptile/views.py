from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Reptile, FeedingLog, FeedingRecord
from .forms import FeedingRecordForm
from .forms import ReptileForm
from django.views import View
from django.utils.dateparse import parse_datetime
import json
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def reptile_detail(request, id):
    reptile = get_object_or_404(Reptile, pk=id)
    return render(request, 'reptile_detail.html', {'reptile': reptile})

def home(request):
    return render(request, 'home.html')

def index(request):
    """ カレンダー画面 """
    return render(request, "calender.html")


def edit_reptile_profile(request, reptile_id):
    reptile = get_object_or_404(Reptile, id=reptile_id, owner=request.user)
    if request.method == 'POST':
        form = ReptileForm(request.POST, request.FILES, instance=reptile)
        if form.is_valid():
            form.save()
            return redirect('reptile_profile', reptile_id=reptile.id)
    else:
        form = ReptileForm(instance=reptile)

    return render(request, 'edit_reptile_profile.html', {'form': form, 'reptile': reptile})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('calender')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def reptile_profile(request, reptile_id):
    # 飼育個体を取得。所有者がリクエストユーザーであることを確認。
    try:
        reptile = get_object_or_404(Reptile, id=reptile_id, owner=request.user)
    except Http404:
        messages.error(request, "指定された飼育個体が見つかりません。")
        return redirect('reptile_list')  # 飼育個体一覧にリダイレクト

    # 飼育個体の餌やり記録を取得
    feeding_records = FeedingRecord.objects.filter(reptile=reptile).order_by('-date')

    # テンプレートに渡すコンテキスト
    context = {
        'reptile': reptile,
        'feeding_records': feeding_records,  # 餌やり記録も渡す
    }
    
    return render(request, 'reptile_profile.html', context)

def reptile_list(request):
    reptiles = Reptile.objects.filter(owner=request.user)  # オーナーで絞り込む
    return render(request, 'reptile_list.html', {'reptiles': reptiles})

def add_reptile(request):
    if request.method == 'POST':
        form = ReptileForm(request.POST, request.FILES)
        if form.is_valid():
            reptile = form.save(commit=False)  # まず保存せずにオブジェクトを取得
            reptile.owner = request.user  # オーナーを設定
            reptile.save()  # オブジェクトを保存
            return redirect('reptile_list')
    else:
        form = ReptileForm()

    return render(request, 'add_reptile.html', {'form': form})

def create_feeding_record(request):
    reptiles = Reptile.objects.filter(owner=request.user)
    form = FeedingRecordForm()

    if request.method == 'POST':
        form = FeedingRecordForm(request.POST, request.FILES)

        if form.is_valid():
            feeding_record = form.save(commit=False)
            reptile = get_object_or_404(Reptile, id=form.cleaned_data['reptile'].id, owner=request.user)
            feeding_record.reptile = reptile
            
            # データを保存
            try:
                feeding_record.save()
                # 飼育個体の体重を更新
                reptile.weight = feeding_record.weight
                reptile.save()

                messages.success(request, f"{reptile.name}の体重が{feeding_record.weight}gに更新されました。")
                return redirect('calender')
            except Exception as e:
                messages.error(request, f"記録の保存中にエラーが発生しました: {e}")
        else:
            # フォームのエラーと送信されたデータを表示
            print("フォームエラー:", form.errors)
            print("送信されたデータ:", request.POST)
            print("送信されたファイル:", request.FILES)
            messages.error(request, f"フォームの入力に誤りがあります: {form.errors}")

    return render(request, 'feeding_list.html', {'form': form, 'reptiles': reptiles})

def feeding_logs_api(request):
    feeding_records = FeedingRecord.objects.filter(reptile__owner=request.user).values(
        'date', 'food_type', 'health_status', 'memo', 'reptile__name','feces_and_urine','care_items','shedding','weight'
    )

    events = []
    for record in feeding_records:
        events.append({
            'title': f"{record['reptile__name']} に餌やり",
            'start': record['date'].isoformat(),
            'description': f" {record['memo']}\n餌の種類: {record['food_type']}\n健康状態: {record['health_status']}\n体重: {record['weight']}\nふんの状態: {record['feces_and_urine']}\nケア: {record['care_items']}\n脱皮: {record['shedding']}",
            'color': '#32CD32'  # 美しい緑の色
        })

    return JsonResponse(events, safe=False)


def calender_view(request):
    feeding_records = FeedingRecord.objects.filter(reptile__owner=request.user)
    reptiles = Reptile.objects.filter(owner=request.user)  # 飼育個体を取得
    events = [
        {
            'title': record.reptile.name,
            'start': record.date.isoformat(),
            'extendedProps': {
                'description': record.memo,  # notesの代わりにmemoを使用
            }
        }
        for record in feeding_records
    ]
    return render(request, 'calender.html', {'events': json.dumps(events), 'reptiles': reptiles})  # reptilesを追加

def weight_history(request, reptile_id):
    # 飼育個体を取得
    reptile = get_object_or_404(Reptile, id=reptile_id, owner=request.user)

    # 体重履歴を取得
    dates = []
    weights = []
    
    # FeedingRecordをデータベースから取得
    records = FeedingRecord.objects.filter(reptile=reptile).order_by('date')

    # デバッグ用にレコードを出力
    print(f"Feeding Records for {reptile.name}:")
    for record in records:
        print(f"Date: {record.date}, Weight: {record.weight}")  # 体重があるか確認
        if record.weight is not None:
            dates.append(record.date.strftime('%Y-%m-%d'))
            weights.append(float(record.weight))

    # 所有する飼育個体を取得（ドロップダウン用）
    reptiles = Reptile.objects.filter(owner=request.user)

    # デバッグ用に最終的なリストを出力
    print("Final dates:", dates)
    print("Final weights:", weights)

    # JSON形式でデータを返す
    return render(request, 'weight_history.html', {
        'reptile': reptile,
        'reptiles': reptiles,
        'dates': json.dumps(dates),  # JavaScriptで使えるようにJSON形式に変換
        'weights': json.dumps(weights),
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
    return render(request, 'feeding_record_list.html', {'feeding_records': records, 'reptiles': reptiles})
def feeding_record_count(request):
    try:
        # 月別の餌やり回数を集計
        feeding_counts = FeedingRecord.objects.filter(
            reptile__owner=request.user
        ).annotate(month=TruncMonth('date'))  # 月ごとに集計
        feeding_counts = feeding_counts.values('month').annotate(count=Count('id')).order_by('month')

        # 月別データを整理
        months = []
        counts = []

        for record in feeding_counts:
            months.append(record['month'].strftime('%Y-%m'))  # YYYY-MM 形式に変換
            counts.append(record['count'])  # 餌やり回数

        # デバッグ用：データをログに出力
        print("Months:", months)
        print("Counts:", counts)

    except FeedingRecord.DoesNotExist:
        # データが存在しない場合の処理
        months = []
        counts = []
        print("No feeding records found for the current user.")

    except Exception as e:
        # その他の例外処理
        months = []
        counts = []
        print(f"An error occurred: {e}")

    # JSON 形式でデータを返す
    return JsonResponse({
        'months': months,
        'counts': counts,
    })


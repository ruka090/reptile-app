from django import forms
from .models import Reptile,FeedingRecord

class ReptileForm(forms.ModelForm):
    class Meta:
        model = Reptile
        fields = [
            'name', 
            'species', 
            'thumbnail', 
            'morph', 
            'acquisition_date', 
            'feeding_schedule', 
            'health_notes', 
            'weight'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': '名前を入力してください'}),
            'species': forms.TextInput(attrs={'placeholder': '種別を入力してください'}),
            'thumbnail': forms.ClearableFileInput(attrs={'placeholder': 'サムネイル画像を選択'}),
            'acquisition_date': forms.DateInput(attrs={'type': 'date'}),
            'feeding_schedule': forms.TextInput(attrs={'placeholder': '餌やりのスケジュールを入力'}),
            'health_notes': forms.Textarea(attrs={'placeholder': '健康に関するメモを入力'}),
            'weight': forms.NumberInput(attrs={'placeholder': '体重を入力してください'}),
        }
        labels = {
            'name': '名前',
            'species': '種別',
            'thumbnail': 'サムネイル',
            'morph': 'モルフ',
            'acquisition_date': '取得日',
            'feeding_schedule': '餌やりスケジュール',
            'health_notes': '健康ノート',
            'weight': '体重',
        }

class FeedingRecordForm(forms.ModelForm):
    class Meta:
        model = FeedingRecord
        fields = ['reptile', 'date', 'food_type', 'memo', 'weight', 'health_status', 'care_items', 'image', 'feces_and_urine', 'shedding']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'food_type': forms.TextInput(attrs={'placeholder': '餌の種類を入力してください'}),
            'memo': forms.Textarea(attrs={'placeholder': 'メモを入力してください'}),
            'health_status': forms.Select(choices=[
                ('very_good', 'かなり良好'),
                ('good', '良好'),
                ('normal', '普通'),
                ('slightly_bad', '少し悪い'),
                ('very_bad', 'かなり悪い'),
            ]),
            'care_items': forms.Select(choices=[
                ('掃除', '掃除'),
                ('温浴', '温浴'),
                ('ハンドリング', 'ハンドリング'),
                ('水替え', '水替え'),
            ]),
            'feces_and_urine' : forms.Select(choices=[
        ('いい', 'いい'),
        ('わるい', 'わるい'),
    ]),
            'shedding' : forms.Select(choices=[
        ('白濁', '白濁'),
        ('脱皮', '脱皮'),
    ])
        }
        labels = {
            'reptile': '飼育個体',
            'date': '日付',
            'food_type': '餌の種類',
            'memo': 'メモ',
            'weight': '体重 (g)',
            'image': '画像',
            'health_status': '調子',
            'care_items': 'ケア項目',
        }

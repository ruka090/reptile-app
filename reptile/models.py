from django.db import models
from django.contrib.auth.models import User

class Reptile(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    thumbnail = models.ImageField(null=True, blank=True)
    morph = models.CharField(max_length=100, blank=True)
    acquisition_date = models.DateField()
    feeding_schedule = models.TextField()
    health_notes = models.TextField()
    weight = models.DecimalField(
    max_digits=5, decimal_places=1, verbose_name='体重 (g)', null=True, blank=True
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class FeedingRecord(models.Model):
    REPTILE_CARE_CHOICES = [
        ('掃除', '掃除'),
        ('温浴', '温浴'),
        ('ハンドリング', 'ハンドリング'),
                ('水替え', '水替え'),
    ]
    HEALTH_STATUS_CHOICES = [
    ('very_good', 'かなり良好'),
    ('good', '良好'),
    ('normal', '普通'),
    ('slightly_bad', '少し悪い'),
    ('very_bad', 'かなり悪い'),
]

    reptile = models.ForeignKey(Reptile, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    food_type  = models.CharField(max_length=255, null=True)
    memo = models.TextField(blank=True)
    weight = models.DecimalField(
    max_digits=5, decimal_places=1, verbose_name='体重 (g)', null=True, blank=True
    )
    health_status = models.CharField(max_length=20, choices=HEALTH_STATUS_CHOICES, null=True, blank=True)
    care_items = models.CharField(max_length=255, null=True, blank=True) 
 # 複数選択のためTextFieldに変更
    image = models.ImageField(null=True, blank=True)
    feces_and_urine = models.CharField(max_length=10, choices=[
        ('いい', 'いい'),
        ('わるい', 'わるい'),
    ], blank=True)  # ふんと尿の状態
    shedding = models.CharField(max_length=10, choices=[
        ('白濁', '白濁'),
        ('脱皮', '脱皮'),
    ], blank=True)  # 脱皮の状態
    def save(self, *args, **kwargs):
        # 複数選択されたケア項目をカンマ区切りで保存
        if isinstance(self.care_items, list):
            self.care_items = ','.join(self.care_items)
        super().save(*args, **kwargs)

    def get_care_items_list(self):
        # 保存されたケア項目をリストとして取得
        return self.care_items.split(',') if self.care_items else []


class WeightRecord(models.Model):
    reptile = models.ForeignKey(Reptile, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.FloatField()

    def __str__(self):
        return f"{self.reptile.name} - {self.date} - {self.weight}g"

class FeedingLog(models.Model):
    # フィールドの定義
    reptile = models.ForeignKey(Reptile, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    food_type = models.CharField(max_length=255, null=True)
    memo = models.TextField(blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)

    def __str__(self):
        return f"{self.reptile.name}の餌やり記録 ({self.date})"


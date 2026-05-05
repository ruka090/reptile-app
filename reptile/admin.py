from django.contrib import admin
from .models import Reptile, FeedingLog, FeedingRecord, WeightRecord

class WeightRecordAdmin(admin.ModelAdmin):
    list_display = ('reptile', 'date', 'weight')
    search_fields = ('reptile__name',)
    list_filter = ('date',)

admin.site.register(Reptile)
admin.site.register(FeedingLog)
admin.site.register(FeedingRecord)
admin.site.register(WeightRecord, WeightRecordAdmin)

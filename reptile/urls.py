from django.conf import settings
from django.urls import path

from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # トップページ
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('feeding/record/create/', views.create_feeding_record, name='create_feeding_record'),  # 修正点
    path('reptiles/', views.reptile_list, name='reptile_list'),  # 重複削除
    path('add_reptile/', views.add_reptile, name='add_reptile'),
    path('profile/<int:reptile_id>/', views.reptile_profile, name='reptile_profile'),
    path('profile/<int:reptile_id>/edit/', views.edit_reptile_profile, name='edit_reptile_profile'),
    #path('feed_reptile/', views.feed_reptile, name='feed_reptile'),
    path('calender/', views.calender_view, name='calender'),  # カレンダーのURLを統一
    #path('reptile/<int:reptile_id>/weight-history/', views.weight_history, name='weight_history'),
    path('api/feeding-logs/', views.feeding_logs_api, name='feeding_logs_api'),  # 重複削除
    path('feeding-records/', views.feeding_record_list, name='feeding_record_list'),  # 餌やり記録一覧
    path('api/weight-history/<int:reptile_id>/', views.weight_history, name='weight_history'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# メディアファイルの設定（必要な場合）





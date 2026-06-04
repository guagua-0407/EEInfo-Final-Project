from django.urls import path
from . import views

urlpatterns = [
    # 首頁 (全系公佈欄 + 網格系隊列表)
    path('', views.team_list, name='team_list'), 
    
    # 行事曆相關 (你剛剛加的功能，原封不動保留)
    path('calendar/', views.calendar_page, name='calendar_page'),
    path('api/events/', views.get_events, name='get_events'),
    
    path('announcement/<int:pk>/', views.announcement_detail, name='announcement_detail'),
path('curriculum/', views.curriculum_page, name='curriculum_page'),
    # 個別系隊頁面 (為了網址好看，加上 team/ 前綴)
    path('team/<int:team_id>/', views.team_detail, name='team_detail'),
    path('team/<int:team_id>/announce/', views.create_announcement, name='create_announcement'),
    path('team/<int:team_id>/edit/', views.edit_team, name='edit_team'),
    path('team/<int:team_id>/event/', views.create_event, name='create_event'),
]
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 【修改這裡】把 'teams/' 變成空字串 ''
    path('', include('teams.urls')), 
    
    path('accounts/', include('django.contrib.auth.urls')), 
]
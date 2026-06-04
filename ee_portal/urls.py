from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 【修改這裡】把 'teams/' 變成空字串 ''
    path('', include('teams.urls')), 
    
    path('accounts/', include('django.contrib.auth.urls')), 
]

# 開發環境下提供媒體檔案服務
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
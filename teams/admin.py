from django.contrib import admin
from .models import Team, Announcement, DepartmentAnnouncement, Event, Tag

admin.site.register(Team)
admin.site.register(Announcement)
# admin.site.register(DepartmentAnnouncement) # <-- 註冊到後台
admin.site.register(Event)

@admin.register(DepartmentAnnouncement)
class DepartmentAnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at') # 後台列表顯示欄位
    list_filter = ('category', 'tags')                 # 後台右側過濾器
    filter_horizontal = ('tags',)
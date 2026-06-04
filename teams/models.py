from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name="系隊/團體名稱")
    description = models.TextField(verbose_name="簡介")
    
    # 【修改這裡】使用 ManyToManyField，讓一個團隊可以有多個學生來管理
    managers = models.ManyToManyField(User, related_name='managed_teams', blank=True, verbose_name="頁面管理員")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Announcement(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.team.name}] {self.title}"
    
# teams/models.py 的最下方新增：
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="標籤名稱")

    def __str__(self):
        return self.name
    
class DepartmentAnnouncement(models.Model):
    # 定義分類的選項
    CATEGORY_CHOICES = [
        ('activity', '學生活動'),
        ('admin', '校務行政'),
        ('admission', '升學資訊'),
        ('notice', '系上通知'),
        ('honor', '榮譽榜'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="公告標題")
    
    # 新增：單選分類 (預設為系上通知)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='notice', verbose_name="分類")
    
    # 新增：多選標籤 (blank=True 代表公告也可以不加標籤)
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="標籤")
    
    content = models.TextField(verbose_name="公告內容")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="發布者")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"

class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="活動名稱")
    description = models.TextField(verbose_name="活動說明", blank=True)
    start_time = models.DateTimeField(verbose_name="開始時間")
    end_time = models.DateTimeField(verbose_name="結束時間")
    
    # 綁定主辦單位 (可以為空，代表是全系通用活動)
    team = models.ForeignKey('Team', on_delete=models.CASCADE, null=True, blank=True, related_name='events', verbose_name="主辦系隊")

    def __str__(self):
        return self.title

# 1. 新增標籤模型


# 2. 升級系級公告模型

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.timezone import localtime
from .models import Team, Announcement, DepartmentAnnouncement, Event, Tag

def calendar_page(request):
    return render(request, 'teams/calendar.html')

def get_events(request):
    events = Event.objects.all()
    event_list = []
    
    for event in events:
        event_list.append({
            'title': event.title,
            # ISO 格式是 FullCalendar 看得懂的時間格式
            'start': localtime(event.start_time).isoformat(), 
            'end': localtime(event.end_time).isoformat(),
            # 如果這個活動有綁定系隊，點擊活動就跳轉到該系隊頁面
            'url': f'/teams/{event.team.id}/' if event.team else '',
        })
        
    return JsonResponse(event_list, safe=False)

# 1. 升級原本的 team_detail：把該系隊的活動也撈出來顯示
def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    announcements = team.announcements.all().order_by('-created_at')
    
    # 撈出屬於這個系隊的活動，並依照時間排序
    team_events = team.events.all().order_by('start_time')
    
    can_edit = False
    if request.user.is_authenticated:
        can_edit = request.user in team.managers.all()

    return render(request, 'teams/team_detail.html', {
        'team': team,
        'announcements': announcements,
        'team_events': team_events, # 傳給前端
        'can_edit': can_edit
    })

# 2. 新增：編輯系隊資訊
@login_required
def edit_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.user not in team.managers.all():
        return redirect('team_detail', team_id=team.id)

    if request.method == "POST":
        team.description = request.POST.get('description')
        team.save()
        return redirect('team_detail', team_id=team.id)
        
    return render(request, 'teams/edit_team.html', {'team': team})

# 3. 新增：建立系隊活動 (行事曆)
@login_required
def create_event(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.user not in team.managers.all():
        return redirect('team_detail', team_id=team.id)

    if request.method == "POST":
        title = request.POST.get('title')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        description = request.POST.get('description', '')
        
        Event.objects.create(
            title=f"[{team.name}] {title}", # 自動在標題加上系隊名稱
            start_time=start_time,
            end_time=end_time,
            description=description,
            team=team # 綁定主辦系隊
        )
        return redirect('team_detail', team_id=team.id)
        
    return render(request, 'teams/create_event.html', {'team': team})

@login_required
def create_announcement(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    
    # 【修改這裡】如果當前登入的學生不是該隊的 manager，就踢回上一頁
    if request.user not in team.managers.all():
        return redirect('team_detail', team_id=team.id)

    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        Announcement.objects.create(
            team=team,
            title=title,
            content=content,
            author=request.user
        )
        return redirect('team_detail', team_id=team.id)
        
    return render(request, 'teams/create_announcement.html', {'team': team})

# teams/views.py 新增這個函數
def team_list(request):
    teams = Team.objects.all()
    # 預設抓取所有公告
    announcements = DepartmentAnnouncement.objects.all().order_by('-created_at')
    
    # 抓出所有的標籤跟分類選項，要傳給前端畫按鈕
    all_tags = Tag.objects.all()
    categories = DepartmentAnnouncement.CATEGORY_CHOICES
    
    # 接收網址傳來的篩選條件
    category_filter = request.GET.get('category')
    tag_filter = request.GET.get('tag')
    
    if category_filter:
        announcements = announcements.filter(category=category_filter)
    if tag_filter:
        # __name 代表跨關聯查詢，尋找標籤名稱等於傳入值的公告
        announcements = announcements.filter(tags__name=tag_filter)

    return render(request, 'teams/team_list.html', {
        'teams': teams,
        'global_announcements': announcements,
        'all_tags': all_tags,
        'categories': categories,
        'current_category': category_filter,
        'current_tag': tag_filter,
    })

# teams/views.py 的最下面加上這個：

def announcement_detail(request, pk):
    # 根據網址傳來的 pk (主鍵 ID) 撈出該篇公告，找不到就報 404
    post = get_object_or_404(DepartmentAnnouncement, pk=pk)
    return render(request, 'teams/announcement_detail.html', {'post': post})

# teams/views.py 新增這行：
def curriculum_page(request):
    return render(request, 'teams/curriculum.html')

@login_required
def create_department_announcement(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category', 'notice')
        author_name = request.POST.get('author_name', '')
        
        # 建立一個臨時使用者或直接存儲名字
        announcement = DepartmentAnnouncement.objects.create(
            title=title,
            content=content,
            category=category,
            author=request.user if request.user.is_authenticated else None
        )
        
        # 如果有提交標籤，就加上去
        tag_names = request.POST.getlist('tags')
        for tag_name in tag_names:
            if tag_name:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                announcement.tags.add(tag)
        
        return redirect('team_list')
    
    all_tags = Tag.objects.all()
    categories = DepartmentAnnouncement.CATEGORY_CHOICES
    
    return render(request, 'teams/create_department_announcement.html', {
        'all_tags': all_tags,
        'categories': categories,
    })
#!/bin/bash

# 清空主项目数据库
echo "🧹 正在清空主项目数据库中的公告..."
cd /home/wayne/Desktop/EEInfo-project
source venv/bin/activate
python manage.py shell << PYTHON_CMD
from teams.models import DepartmentAnnouncement, Announcement

# 1. 清空所有「系級公告」
dept_count = DepartmentAnnouncement.objects.count()
DepartmentAnnouncement.objects.all().delete()
print(f'✓ 已清空 {dept_count} 篇系級公告 (DepartmentAnnouncement)')

# 2. 清空所有「系隊專屬公告」
announce_count = Announcement.objects.count()
Announcement.objects.all().delete()
print(f'✓ 已清空 {announce_count} 篇系隊公告 (Announcement)')

print(f'\n✓ 完成！共清空 {dept_count + announce_count} 篇公告')
PYTHON_CMD

echo ""
echo "🧹 正在清空 worktree 数据库中的公告..."
cd /home/wayne/Desktop/EEInfo-project.worktrees/agents-clear-previous-announcements
source /home/wayne/Desktop/EEInfo-project/venv/bin/activate
python manage.py shell << PYTHON_CMD
from teams.models import DepartmentAnnouncement, Announcement

# 1. 清空所有「系級公告」
dept_count = DepartmentAnnouncement.objects.count()
DepartmentAnnouncement.objects.all().delete()
print(f'✓ 已清空 {dept_count} 篇系級公告 (DepartmentAnnouncement)')

# 2. 清空所有「系隊專屬公告」
announce_count = Announcement.objects.count()
Announcement.objects.all().delete()
print(f'✓ 已清空 {announce_count} 篇系隊公告 (Announcement)')

print(f'\n✓ 完成！共清空 {dept_count + announce_count} 篇公告')
PYTHON_CMD

echo ""
echo "✅ 全部完成！所有公告已清空！"

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # 1. 정렬 기준을 이메일로 변경 (에러 해결의 핵심)
    ordering = ('email',)
    
    # 2. 관리자 목록 화면에 보여질 항목들 (username 제거)
    list_display = ('email', 'nickname', 'age', 'is_staff', 'is_active')
    
    # 3. 검색 창에서 검색할 필드 (username 제거)
    search_fields = ('email', 'nickname')

    # 4. 관리자 페이지 수정 폼 구성 (username 필드 제거)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('nickname', 'age')}), # 여기에 커스텀 필드 추가
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
# Register your models here.
admin.site.register(User, CustomUserAdmin)
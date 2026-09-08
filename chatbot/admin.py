from django.contrib import admin
from .models import Course, Branch, Fee, FAQ, Facility, Contact, ChatMessage


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'degree', 'duration')
    search_fields = ('name', 'degree')


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'course')
    list_filter = ('course',)
    search_fields = ('name',)


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('course', 'amount', 'additional_fee', 'academic_year')
    list_filter = ('academic_year', 'course')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'intent')
    list_filter = ('intent',)
    search_fields = ('question', 'answer')


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('department', 'phone', 'email')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user_message', 'bot_response', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

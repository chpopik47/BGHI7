from django.contrib import admin

from .models import Room, Topic, Message, User, InvitationCode, PostVote


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ('id', 'email', 'username', 'affiliation', 'is_paid', 'is_staff', 'is_active')
    list_filter = ('affiliation', 'is_paid', 'is_staff', 'is_active')
    search_fields = ('email', 'username', 'name')

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)


@admin.register(InvitationCode)
class InvitationCodeAdmin(admin.ModelAdmin):

    list_display = ('code', 'is_active', 'used_at', 'used_by', 'created_at')
    search_fields = ('code',)
    list_filter = ('is_active', 'used_at')


@admin.register(PostVote)
class PostVoteAdmin(admin.ModelAdmin):

    list_display = ('room', 'user', 'value', 'created_at')
    list_filter = ('value', 'created_at')

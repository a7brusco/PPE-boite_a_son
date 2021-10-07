from django.contrib import admin
from .models import *
import pprint
from django.contrib.sessions.models import Session
from django.templatetags.static import static
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class SampleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        ('Date information', { 'fields' : ['created_date']}),
        ('Author', { 'fields' : ['user']}),
        ('Users', {'fields' : ['users']}),
        ('Tag', { 'fields' : ['tag']}),
        ('Audio file', { 'fields' : ['file']}),
        ('Macro/Micro Sample', {'fields' : ['isMacro']}),
        ('Private/Public Sample', {'fields' : ['isPublic']}),
        ('Background Image', {'fields' : ['background']}),]

class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        ('Date information', { 'fields' : ['created_date']}),
        ('Author', { 'fields' : ['user']}),
        ('Json file', { 'fields' : ['file']})]


class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User', {'fields': ['user']}),
        ('Biographie', { 'fields' : ['bio']}),
        ('Favorite Music SoftWare', {'fields' : ['favMusicSoftware']}),
        ('Music Style', { 'fields' : ['musicStyle']}),
        ('image', { 'fields' : ['image']}),]

class KitAdmin(admin.ModelAdmin):
    fieldsets = [
        ('SampleList', {'fields':['sampleList']}),
        ('User', {'fields' : ['user']}),
    ]
    
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

class TagAdmin(admin.ModelAdmin):
    pass

class CollectionAdmin(admin.ModelAdmin):
    pass

class BackgroundAdmin(admin.ModelAdmin):
    fieldsets=[('Image', {'fields':['image']}),]

class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return pprint.pformat(obj.get_decoded()).replace('\n', '<br>\n')
    _session_data.allow_tags=True
    list_display = ['session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']
    exclude = ['session_data']
    date_hierarchy='expire_date'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Kit, KitAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Background, BackgroundAdmin)

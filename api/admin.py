from django.contrib import admin
from .models import *
from mod import get_module
from django.contrib.auth.models import User, Group

class MessagePropertyInline(admin.TabularInline):
    model = MessageProperty
    extra = 0

class MessageAdmin(admin.ModelAdmin):
    inlines = [
            MessagePropertyInline
        ]
    list_filter = [('is_series_head')]

class ModuleAssetInline(admin.TabularInline):
    model = ModuleAsset
    extra = 0

class ModuleAdmin(admin.ModelAdmin):
    inlines = [
            ModuleAssetInline
        ]

    def get_fieldsets(self, request, obj=None):
        fs = super(ModuleAdmin, self).get_fieldsets(request, obj)
        if obj:
            po = get_module(obj.name)
            if po:
                a, b = fs[0]
                b["fields"].remove("name")
                doc = type(po).__doc__
                if doc:
                    from markdown import markdown
                    b["description"] = markdown(doc)
        return fs

    def has_add_permission(self, request):
        return False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        q = Module.objects.filter(pk=object_id).first()
        if q:
            extra_context['title'] = "Configure module " + q.name
        return super(ModuleAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

class PatchewAdminSite(admin.AdminSite):
    site_header = 'Patchew admin'
    site_title = 'Patchew admin'
    index_title = 'Patchew administration'

admin_site = PatchewAdminSite()

admin_site.register(Project)
admin_site.register(Message, MessageAdmin)
admin_site.register(Module, ModuleAdmin)
admin_site.register(User)
admin_site.register(Group)

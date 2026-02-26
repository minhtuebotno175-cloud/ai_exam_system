from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['filename', 'user', 'file_type', 'status', 'created_at']
    list_filter = ['status', 'file_type', 'created_at']
    search_fields = ['filename', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
from django.contrib import admin
from rango.models import Category, Page

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}    #预填充领域

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

# Register your models here.
# 注册类
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
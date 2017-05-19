from django.contrib import admin

# Register your models here.
from blog.models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'timestamp', 'updated']  # 项目显示
    list_display_links = ['title','updated']  # 按更新日链接
    # list_editable = ['title']  #项目可编辑
    list_filter = ['timestamp', 'updated']  # ex日期过滤器
    search_fields = ['title', 'content']

    class Meta:
        model = Article


admin.site.register(Article, ArticleAdmin)

from django.contrib import admin

from models import News


class NewsAdmin(admin.ModelAdmin):
    """
    Admin interface class for news model
    """
    list_display = ("title", "user", "date")
    search_fields = ("title", "content")
    list_filter = ("user",)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

admin.site.register(News, NewsAdmin)

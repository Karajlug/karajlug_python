# -----------------------------------------------------------------------------
#    Karajlug.org
#    Copyright (C) 2010  Karajlug community
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# -----------------------------------------------------------------------------

from django.contrib import admin

from .models import Book


class BookAdmin(admin.ModelAdmin):
    """
    Admin interface for book model.
    """
    list_display = ("__unicode__", "url", "completed",
                    "online_book", "creator")
    list_editable = ("url", )
    search_fields = ("name", )
    list_filter = ("creator", )
    prepopulated_fields = {"slug": ("name",)}

    fieldsets = (
        (None, {
            'fields': ('language', ('name', 'slug', 'online_book',
                                    'completed'),
                       ('maintainers', 'weight'))
        }),
        ('Optional Fields', {
            'classes': ('collapse',),
            'fields': ('cover', ('isbn', 'license'),
                       ('url', 'downloadlink'), 'desc')
        })
    )

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        obj.save()


admin.site.register(Book, BookAdmin)

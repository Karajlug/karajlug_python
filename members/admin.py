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

from models import Member, MemberDetail


class MemberAdmin(admin.ModelAdmin):
    """
    Admin interface class for member model
    """
    list_display = ("name", "link", "mail", "user")
    list_editable = ("link", "mail")
    search_fields = ("name", "mail")
    list_filter = ("user",)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


class DetailAdmin(admin.ModelAdmin):
    """
    Admin interface class for member detail model
    """
    list_display = ("member", "field_name", "field_value", "user", "language")
    list_editable = ("field_name", "field_value", "language")
    search_fields = ("member", "filed_name")
    list_filter = ("user", "member")

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

admin.site.register(Member, MemberAdmin)
admin.site.register(MemberDetail, DetailAdmin)

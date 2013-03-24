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
from django.core.exceptions import PermissionDenied
from django.contrib.admin import widgets, helpers
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.forms.formsets import all_valid
from django.forms.util import ErrorList

from .models import Member, MemberDetail


def email(obj):
    return obj.user.email
email.short_description = "Email"


class MemberAdmin(admin.ModelAdmin):
    list_display = ("user", "link", "avatar", "weight", "creator")
    ordering = ("weight", )
    list_editable = ("weight", )
    search_fields = ("name", )
    list_filter = ("creator", )

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        obj.save()


class MemberDetailsAdmin(admin.ModelAdmin):
    list_display = ("language", "member", "field_name", "field_value", "user",
                    "weight")
    ordering = ("weight", )
    list_editable = ("weight", )
    search_fields = ("member", )

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        obj.save()

admin.site.register(Member, MemberAdmin)
admin.site.register(MemberDetail, MemberDetailsAdmin)

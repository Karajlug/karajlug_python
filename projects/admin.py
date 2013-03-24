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
from django.utils.translation import ugettext as _

from .models import Project, Repository


class ProjectAdmin(admin.ModelAdmin):
    """
    Admin interface class for project model
    """
    list_display = ("__unicode__", "version", "home", "license", "vcs",
                    "creator", "weight")
    ordering = ("weight", )
    list_editable = ("home", "weight")
    search_fields = ("name", )
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("creator", )

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        obj.save()


class RepositoryAdmin(admin.ModelAdmin):
    """
    Admin interface class for repository model
    """
    list_display = ("project", "address", "weight")
    list_editable = ("address", "weight")
    ordering = ("weight", )
    search_fields = ("project", )
    list_filter = ("project", )


admin.site.register(Project, ProjectAdmin)
admin.site.register(Repository, RepositoryAdmin)

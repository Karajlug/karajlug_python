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

def email(obj):
    return obj.user.emial


class MemberAdmin(admin.ModelAdmin):
    """
    Admin interface class for member model
    """
    list_display = ("__unicode__", "link", email, "user")
    list_editable = ("link", )
    search_fields = ("user", "user__email")
    list_filter = ("user", )

    def save_model(self, request, obj, form, change):
        if request.user == obj.user or request.user.is_superuser or \
               request.user.has_perm("members.member_admin"):
            obj.creator = request.user
            if not request.user.is_superuser or \
               not request.user.has_perm("members.member_admin"):
                if change:
                    obj.weight = Member.objects.filter(id=obj.id)[0].weight
                else:
                    obj.weight = 40
            obj.save()
        else:
            return 

    def queryset(self, request):
        """
        Return the records that user allowed to see.
        """
        if request.user.is_superuser or request.user.has_perm("members.member_admin"):
            return Member.objects.all()
        else:
            return Member.objects.filter(user = request.user)


class DetailAdmin(admin.ModelAdmin):
    """
    Admin interface class for member detail model
    """
    list_display = ("member", "field_name", "field_value", "user", "language")
    list_editable = ("field_name", "field_value", "language")
    search_fields = ("member", "filed_name")
    list_filter = ("user", "member")

    def save_model(self, request, obj, form, change):
        if request.user == obj.member or request.user.is_superuser or \
               request.user.has_perm("members.member_admin"):
            obj.user = request.user
            obj.save()
        else:
            return

    def queryset(self, request):
        """
        Return the records that user allowed to see.
        """
        if request.user.is_superuser or request.user.has_perm("members.member_admin"):
            return MemberDetail.objects.all()
        else:
            return MemberDetail.objects.filter(member = request.user)


admin.site.register(Member, MemberAdmin)
admin.site.register(MemberDetail, DetailAdmin)

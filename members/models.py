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

from django.db import models
from django.utils.translation import ugettext as _


class Member(models.Model):
    """
    Member model of karajlug.
    """

    name = models.CharField(max_length=32,
                            verbose_name=_("Name"))
    link = models.URLField(verbose_name=_("Home Page"),
                           blank=True, null=True)
    mail = models.CharField(verbose_name=_("Email"),
                            max_length=64,
                            blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True,
                               upload_to="uploads/avarars/",
                               verbose_name=_("Avatar"))
    weight = models.IntegerField(default=40, verbose_name=_("Item Weight"))


    desc = models.TextField(verbose_name=_("Description"),
                            blank=True, null=True)
    user = models.ForeignKey("auth.User", verbose_name=_("Creator"),
                             editable=False)


    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Member")
        verbose_name_plural = _("Members")


class MemberDetail(models.Model):
    """
    Details of each memeber.
    """
    LANGUAGES = [
        ["0", "en-us"],
        ["1", "fa"],
    ]

    language = models.CharField(choices=LANGUAGES,
                                default="0",
                                max_length=1,
                                verbose_name=_("Language"))

    member = models.ForeignKey(Member, verbose_name=_("Member"))
    field_name = models.CharField(max_length=64,
                                  verbose_name=_("Field Name"))
    field_value = models.CharField(max_length=256)
    weight = models.IntegerField(default=40, verbose_name=_("Item Weight"))

    user = models.ForeignKey("auth.User", verbose_name=_("Creator"),
                             editable=False)

    def __unicode__(self):
        return "%s - %s" % (self.field_name,
                            self.field_value)

    class Meta:
        verbose_name = _("Member Detail")
        verbose_name_plural = _("Member Details")

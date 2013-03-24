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
from django.core.exceptions import ValidationError


class Member(models.Model):
    """
    Member model of karajlug.
    """
    user = models.OneToOneField(
        "auth.User", verbose_name=_("User"),
        related_name="%(app_label)s_%(class)s_related",
        help_text=_("Who is the owner of this profile?"))

    link = models.URLField(verbose_name=_("Home Page"),
                           blank=True, null=True,
                           help_text=_("Home page link"))

    avatar = models.ImageField(
        blank=True, null=True,
        upload_to="uploads/avarars/",
        verbose_name=_("Avatar"),
        help_text=_("Please use your real face avatar. ") +
        _("Size: 128x128 DO NOT UPLOAD BIG FILES !!!"))

    weight = models.IntegerField(default=40, verbose_name=_("Item Weight"),
                                 help_text=_("This field is not important"))

    desc = models.TextField(verbose_name=_("Description"),
                            blank=True, null=True)

    creator = models.ForeignKey("auth.User", verbose_name=_("Creator"),
                                editable=False)

    def __unicode__(self):
        return self.user.get_full_name()

    def fullname(self):
        return self.__unicode__()

    def get_absolute_url(self):
        return "/members/%i/" % self.id

    def safe_email(self):
        """
        use js to hide email.
        """
        template = """
        <SCRIPT LANGUAGE="JavaScript">
        user = '$$username$$';
        site = '$$domain$$';
        document.write('<a href=\"mailto:' + user + '@' + site + '\">');
        document.write(user + '@' + site + '</a>');
        </SCRIPT>
        """
        if self.user.email:
            username, domain = self.user.email.split("@")
            result = template.replace("$$username$$", username).replace(
                "$$domain$$", domain)
            return result
        else:
            return ""

    def full_path(self):
        from django.conf import settings
        site = getattr(settings, "URL", "www.karajlug.org")
        return "%s%s" % (site, self.get_absolute_url())

    def irc_repr(self, logentry):

        if logentry.is_addition():
            return ["New member added by %s - %s" % (
                self.user,
                self.full_path())]

        phrase = ""
        if logentry.is_change():
            phrase = "change"
        elif logentry.is_delete():
            phrase = "delete"

        return ["%s %s a member: %s" % (
            self.user,
            phrase,
            self.full_path())]

    class Meta:
        verbose_name = _("Member")
        verbose_name_plural = _("Members")
        permissions = (
            ("member_admin", _("Can Add new members and details.")),
        )


class MemberDetail(models.Model):
    """
    Details of each memeber.
    """
    LANGUAGES = [
        ["0", "en-us"],
        ["1", "fa"],
    ]

    language = models.CharField(
        choices=LANGUAGES,
        default="0",
        max_length=1,
        verbose_name=_("Language"),
        help_text=_("Site language (en-us at this time)"))

    member = models.ForeignKey(
        Member, verbose_name=_("Member"),
        help_text=_("Who is the owner of this property?"))

    field_name = models.CharField(max_length=64,
                                  verbose_name=_("Field Name"),
                                  help_text=_("Profile property name"))

    field_value = models.CharField(max_length=256)

    weight = models.IntegerField(
        default=40, verbose_name=_("Item Weight"),
        help_text=_("Properties with lower weight will appear sooner."))

    user = models.ForeignKey("auth.User", verbose_name=_("Creator"),
                             editable=False)

    def __unicode__(self):
        return "%s - %s" % (self.field_name,
                            self.field_value)

    def irc_repr(self, logentry):

        if logentry.is_addition():
            return ["Some details added for %s" % (self.member.user)]

        phrase = ""
        if logentry.is_change():
            phrase = "changed"
        elif logentry.is_delete():
            phrase = "deleted"

        return ["A profile detail for %s %s" % (
            self.member.user,
            phrase)]

    class Meta:
        verbose_name = _("Member Detail")
        verbose_name_plural = _("Member Details")

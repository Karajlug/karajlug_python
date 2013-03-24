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


class Book(models.Model):
    """
    Book model
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

    name = models.CharField(max_length=80,
                            verbose_name=_("Book Name"))
    slug = models.SlugField(verbose_name=_("Slug"),
                            unique=True)

    maintainers = models.ManyToManyField(
        "auth.User",
        related_name="%(app_label)s_%(class)s_related",
        verbose_name=_("Maintainers"))

    cover = models.ImageField(
        blank=True,
        null=True,
        upload_to="uploads/covers/",
        verbose_name=_("Book Cover"),
        help_text=_("Size: 128x128 DO NOT UPLOAD BIG FILES !!!"))

    isbn = models.CharField(blank=True, null=True,
                            verbose_name=_("ISBN"),
                            max_length=32)

    license = models.CharField(verbose_name=_("License"),
                               max_length=16,
                               blank=True, null=True)
    url = models.URLField(verbose_name=_("URL"),
                          blank=True, null=True)
    online_book = models.BooleanField(default=False,
                                      verbose_name=_("Online book"))

    completed = models.BooleanField(default=False,
                                    verbose_name=_("Complete"))

    weight = models.IntegerField(
        default=40,
        verbose_name=_("Order"),
        help_text=_("Book will appear in menu respect to this value"))

    desc = models.TextField(verbose_name=_("Description"),
                            blank=True, null=True)

    downloadlink = models.URLField(verbose_name=_("Download URL"),
                                   blank=True, null=True)

    creator = models.ForeignKey("auth.User", verbose_name=_("Creator"),
                                editable=False)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/books/%s/" % self.slug

    def full_path(self):
        from django.conf import settings
        site = getattr(settings, "URL", "www.karajlug.org")
        return "%s%s" % (site, self.get_absolute_url())

    def irc_repr(self, logentry):

        if logentry.is_addition():
            return ["New book added %s by %s at %s" % (
                self.name,
                self.creator,
                self.full_path())]

        phrase = ""
        if logentry.is_change():
            phrase = "change"
        elif logentry.is_delete():
            phrase = "delete"

        return ["%s %s a book: %s" % (
            self.creator,
            phrase,
            self.full_path())]

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

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

    language = models.CharField(choices=LANGUAGES,
                            default="0",
                            max_length=1,
                            verbose_name=_("Language"),
                            help_text=_("Site language (en-us at this time)"))
    name = models.CharField(max_length=80,
                            verbose_name=_("Book Name"))

    maintainer = models.ForeignKey("auth.User",
                                related_name="%(app_label)s_%(class)s_related",
                                verbose_name=_("Maintainer"))
    license = models.CharField(verbose_name=_("License"),
                               blank=True, null=True)
    url = models.URLField(verbose_name=_("URL"),
                          blank=True, null=True)
    online_book = models.BooleanField(default=False,
                                      verbose_name=_("Online book"))

    creator = models.ForeignKey("auth.User", verbose_name=_("Creator"),
                             editable=False)


# -----------------------------------------------------------------------------
#    Karajlug.org
#    Copyright (C) 2010-2012  Karajlug community
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

from django.conf import settings
from django.utils import translation


class I18nMiddleware(object):
    """
    Set the default locale setting of page.
    """
    def process_request(self, request):
        server = request.META["HTTP_HOST"]
        lang = server.split(".")[0]
        if lang == "en":
            translation.activate("en")
        else:
            translation.activate("fa")
        request.LANGUAGE_CODE = translation.get_language()
        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        return None

    def process_template_response(self, request, response):
        return response

    def process_response(self, request, response):
        return response

    def process_exception(self, request, exception):
        return None

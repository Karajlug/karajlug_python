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
from django.shortcuts import render_to_response as rr
from django.http import Http404
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.conf import settings

from .models import Book


def books_index(request):
    """
    Main index of registered books.
    """
    books = Book.objects.all().order_by("weight")
    book_per_page = 4
    try:
        book_per_page = settings.BOOK_IN_PAGE
    except AttributeError:
        pass
    paginator = Paginator(books, book_per_page)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        books_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        # if provided page value in GET was out of range
        books_list = paginator.page(paginator.num_pages)

    return rr("books.html", {"books": books_list},
              context_instance=RequestContext(request))


def book_view(request, slug):
    """
    View of each Book
    """
    try:
        book = Book.objects.get(slug=slug)
    except Book.DoesNotExist:
        raise Http404()
    return rr("book_view.html", {"book": book},
              context_instance=RequestContext(request))

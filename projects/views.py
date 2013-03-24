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
from django.core.paginator import Paginator
from django.template import RequestContext
from django.http import Http404
from django.utils.translation import get_language

from .models import Project, Repository


def projects_index(request):
    """
    project index page
    """
    projects = Project.objects.all().order_by("weight")
    # god damn b3hnam's server
    projects = [(i + 1, j) for i, j in enumerate(projects)]
    # ---
    return rr("projects.html",
              {"projects": projects},
              context_instance=RequestContext(request))


def project_view(request, slug):
    """
    Project view
    """
    try:
        project = Project.objects.get(slug=slug)
    except Project.DoesNotExist:
        raise Http404()

    if project.vcs:
        vcsdict = dict(Project.VCS)
        project.vcs = vcsdict[project.vcs]

    repos = Repository.objects.filter(project=project).order_by("weight")
    return rr("project_view.html",
              {"project": project,
               "repositories": repos},
              context_instance=RequestContext(request))

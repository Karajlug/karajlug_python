from django.shortcuts import render
from django.shortcuts import render_to_response as rr
from django.template import RequestContext
# Create your views here.


def index(request):
    return rr('donate.html',
              {},
              context_instance=RequestContext(request))

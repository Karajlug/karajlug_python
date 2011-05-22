import os
import sys
os.environ['PYTHON_EGG_CACHE'] = '/home/admin/lug.karajiha.ir/python_egg'

sys.path.append(os.path.join (os.path.dirname (__file__) , '../../').replace ("\\" , "/"))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


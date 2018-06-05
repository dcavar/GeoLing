import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'geoling.settings'

def add_python_path():
  root = os.path.dirname(__file__)
  #paths = (os.path.join(root, "packages"),)
  paths = (root,)
  for path in paths:
    if not path in sys.path:
        sys.path.append(path)

#modify path
add_python_path()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

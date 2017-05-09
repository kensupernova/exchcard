#coding:utf-8
"""
WSGI config for exchcard project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys


# # We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# # if running multiple sites in the same mod_wsgi process. To fix this, use
# # mod_wsgi daemon mode with each exchard in its own daemon process, or use
# # os.environ["DJANGO_SETTINGS_MODULE"] = "exchard.settings"
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exchard.settings")
#
# # This application object is used by any WSGI server configured to use this
# # file. This includes Django's development server, if the WSGI_APPLICATION
# # setting points here.


# 添加系统中没有的依赖包
# site_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'exchard-packages'),
# sys.path.insert(0, site_path)

# 设置系统环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exchcard.settings")
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exchard.settings_dev")

# WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
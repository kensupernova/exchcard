import sae
sae.add_vendor_dir('site-packages')

from mysite import wsgi
application = sae.create_wsgi_app(wsgi.application)
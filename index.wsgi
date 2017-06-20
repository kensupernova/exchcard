import sae
import os
import sys

path = os.path.join(os.path.dirname(os.path.abspath('__file__')), 'site-packages')
sae.add_vendor_dir(path)


from exchcard import wsgi
application = sae.create_wsgi_app(wsgi.application)
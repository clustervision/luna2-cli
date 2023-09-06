# import requests
# from requests.adapters import HTTPAdapter
# from requests.packages.urllib3.poolmanager import PoolManager
# import ssl

# class MyAdapter(HTTPAdapter):
#     def init_poolmanager(self, connections, maxsize, block=False):
#         self.poolmanager = PoolManager(num_pools=connections,
#                                        maxsize=maxsize,
#                                        block=block,
#                                        ssl_version=ssl.PROTOCOL_TLSv1)

# s = requests.Session()
# s.mount('https://', MyAdapter())
# s.get('https://host/meters/a_serial/power')



# from urllib3.util import Retry
# from requests import Session
# from requests.adapters import HTTPAdapter

# s = Session()
# retries = Retry(
#     total=3,
#     backoff_factor=0.1,
#     status_forcelist=[502, 503, 504],
#     allowed_methods={'POST'},
# )
# s.mount('https://', HTTPAdapter(max_retries=retries)


# import requests
# from requests.adapters import HTTPAdapter
# from requests.packages.urllib3.util.ssl_ import create_urllib3_context

# # This is the 2.11 Requests cipher string, containing 3DES.
# CIPHERS = (
#     'ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:'
#     'DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+HIGH:RSA+3DES:!aNULL:'
#     '!eNULL:!MD5'
# )


# class DESAdapter(HTTPAdapter):
#     """
#     A TransportAdapter that re-enables 3DES support in Requests.
#     """
#     def init_poolmanager(self, *args, **kwargs):
#         context = create_urllib3_context(ciphers=CIPHERS)
#         kwargs['ssl_context'] = context
#         return super(DESAdapter, self).init_poolmanager(*args, **kwargs)

#     def proxy_manager_for(self, *args, **kwargs):
#         context = create_urllib3_context(ciphers=CIPHERS)
#         kwargs['ssl_context'] = context
#         return super(DESAdapter, self).proxy_manager_for(*args, **kwargs)



import ssl
import requests

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3.util import ssl_

CIPHERS = (
    'ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:'
    'ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:AES256-SHA'
)


class TlsAdapter(HTTPAdapter):

    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(TlsAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, *pool_args, **pool_kwargs):
        ctx = ssl_.create_urllib3_context(ciphers=CIPHERS, cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options)
        self.poolmanager = PoolManager(*pool_args, ssl_context=ctx, **pool_kwargs)


session = requests.session()
adapter = TlsAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
session.mount("https://", adapter)

try:
    r = session.request('GET', 'https://google.com')
    print(r)
except Exception as exception:
    print(exception)
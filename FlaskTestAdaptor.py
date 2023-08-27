import curses
import requests
import connect4_rest
import json
from pprint import pprint as print
import re
from requests import Session
from requests.adapters import BaseAdapter
from urllib.parse import urljoin

class FlaskServerSession(Session):
    def __init__(self, client, base_url=None):
        super().__init__()
        self.flask_client = client
        self.base_url = base_url

    def request(self, method, url, *args, **kwargs):
        joined_url = urljoin(self.base_url, url)
        return super().request(method, joined_url, *args, **kwargs)

    # def send(self, *args, **kwargs):
    #     print(args)
    #     print(args[0].__dict__)
    #     print(kwargs)
    #     print(self.flask_client.__dict__)
    #     # print(dir(self.flask_client))
    #     kwargs

class FlaskClientAdaptor(BaseAdapter):

    def __init__(self, flask_client):
        super().__init__()
        self.client = flask_client

    def send(
        self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None
    ):
        """Sends PreparedRequest object. Returns Response object.

        :param request: The :class:`PreparedRequest <PreparedRequest>` being sent.
        :param stream: (optional) Whether to stream the request content.
        :param timeout: (optional) How long to wait for the server to send
            data before giving up, as a float, or a :ref:`(connect timeout,
            read timeout) <timeouts>` tuple.
        :type timeout: float or tuple
        :param verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use
        :param cert: (optional) Any user-provided SSL certificate to be trusted.
        :param proxies: (optional) The proxies dictionary to apply to the request.
        """
        url = re.sub("http://[^/]*/", "/", request.url)
        method = request.method

        if method == "GET":
            response = self.client.get(url)
        elif method == "POST":
            response = self.client.post(url, data=json.loads(request.body))

        return self.build_response(request, response)

    def build_response(self, req, resp):
        """Builds a :class:`Response <requests.Response>` object from a urllib3
        response. This should not be called from user code, and is only exposed
        for use when subclassing the
        :class:`HTTPAdapter <requests.adapters.HTTPAdapter>`

        :param req: The :class:`PreparedRequest <PreparedRequest>` used to generate the response.
        :param resp: The urllib3 response object.
        :rtype: requests.Response
        """
        from requests import Response
        from requests.models import CaseInsensitiveDict
        from requests.utils import (
            DEFAULT_CA_BUNDLE_PATH,
            extract_zipped_paths,
            get_auth_from_url,
            get_encoding_from_headers,
            prepend_scheme_if_needed,
            select_proxy,
            urldefragauth,
        )
        from requests.cookies import extract_cookies_to_jar
        from io import BytesIO

        response = Response()

        # Fallback to None if there's no status_code, for whatever reason.
        response.status_code = getattr(resp, "_status_code", None)

        # Make headers case-insensitive.
        # response.headers = CaseInsensitiveDict(getattr(resp, "headers", {}))

        # Set encoding.
        # response.encoding = get_encoding_from_headers(response.headers)
        # response.raw = resp
        # response.raw = None

        response.raw = BytesIO(resp.data)
        #response.reason = response.raw.reason
        response.reason = resp._status

        if isinstance(req.url, bytes):
            response.url = req.url.decode("utf-8")
        else:
            response.url = req.url

        # Add new cookies from the server.
        extract_cookies_to_jar(response.cookies, req, resp)

        # Give the Response some context.
        response.request = req
        # response.connection = self

        return response

    def close(self):
        """Cleans up adapter specific items."""
        pass
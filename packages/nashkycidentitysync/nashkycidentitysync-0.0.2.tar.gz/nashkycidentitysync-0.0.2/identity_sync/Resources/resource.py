
from identity_sync.APIs.api_format import API
import json
from identity_sync.APIs.utils.generate_code import get_code


class Resource(API):

    _identity_id = None

    _user_id = None

    _response = {}

    _read_url = ""

    _api = None

    _resource_id = -1

    SMILE = 1
    VERIFY = 2

    @property
    def UPLOAD_IMAGE(self):
        return 0

    def set_identity_id(self, identity_id):
        self._identity_id = identity_id
        return self

    def set_user_id(self, user_id):
        self._user_id = user_id
        return self

    def set_urls(self, urls):
        self.set_read_url(urls.get("read", ""))
        return self

    def read(self, payload=None, method='POST', endpoint=None):
        if endpoint is None:
            endpoint = self.get_read_url()

        # Call the method exec to make the request to A.P.I. endpoint and return the data that will be returned in this method
        self._response = self._exec(payload, method, endpoint)
        return self

    def payload(self):
        return {}

    def serialize(self):
        return self

    def response(self):
        return self._response

    def set_response(self, response={}):
        self._response = response
        return self

    def set_read_url(self, read_url):
        self._read_url = read_url
        return self

    def get_read_url(self):
        return self._read_url

    def get_identity_id(self):
        return self._identity_id

    def get_user_id(self):
        return self._user_id

    def generate_code(self, length=6):
        return get_code(length)

    # This is the method that will be called execute an A.P.I. request.
    # Since most of the A.P.I. calls methods are similar, they are to be placed inside this method to avoid code duplication.
    #
    # It will only accept parameters unique to each A.P.I. request.
    def _exec(self, payload=None, method='POST', endpoint="", files=None):

        if files is None:
            payload = json.dumps(payload)
        else:
            payload = payload

        # Call the iPay A.P.I. url by passing the variables to the super class method responsible for making requests to A.P.I. endpoints
        # The super class method returns a response that is returned by this method
        return super().api_request(url=f"{super().get_base_url()}{endpoint}", payload=payload, method=method, files=files)

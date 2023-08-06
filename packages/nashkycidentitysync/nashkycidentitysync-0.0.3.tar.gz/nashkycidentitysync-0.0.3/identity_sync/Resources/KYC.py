from identity_sync.Resources.resource import Resource
from identity_sync.Resources.identity import Identity


class KYC(Resource):

    _resources = {
        "Identity": Identity(),
    }

    # use the nash object to confirm if the user accessing the identities is logged in
    _nash = None

    urls = {}

    def __init__(self, nash, identity_id=None):
        self._nash = nash
        super().__init__("IdentityAPI", self._nash.get_headers(), self._nash.get_params())
        super().set_identity_id(identity_id)

    def resource(self, resource_name):
        resource = self._resources[resource_name].set_identity_id(
            super().get_identity_id()).set_headers(self._nash.get_headers())

        return resource

    def get_resources(self):
        return list(self._resources.keys())

    def sample_payload(self, identity_id=None, payload = None, method='GET',endpoint="/sample_payload"):

        if identity_id is not None:
            endpoint = f'{endpoint}/{identity_id}'

        return super().read(payload, method, endpoint)

    def identity_types(self, identity_id=None, payload = None, method='GET',endpoint="/identity_types"):

        if identity_id is not None:
            endpoint = f'{endpoint}/{identity_id}'

        return super().read(payload, method, endpoint)

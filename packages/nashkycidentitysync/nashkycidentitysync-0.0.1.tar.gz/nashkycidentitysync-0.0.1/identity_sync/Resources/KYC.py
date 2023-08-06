from identity_sync.Resources.resource import Resource
from identity_sync.Resources.identity import Identity
import json
from identity_sync.settings import SAMPLE_DATA_FILE


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

    def read(self, identity_id=None):
        data = self.identity_types().response()

        identities = data.get("identities",[])

        for i in range(len(identities)):
            identity = identities[i].get("identity",{})

            if identity_id is not None:
                if identity.get("identity_id",0) == identity_id:
                    data = identity
                    break
            elif super().get_identity_id() is not None:
                if identity.get("identity_id",0) == super().get_identity_id():
                    data = identity
                    break

        return super().set_response(response=data)

    def sample_payload(self, identity_id=None):

        data = {}

        json_file = ""

        if identity_id == super().SMILE:
            json_file = "smile"

        elif identity_id == super().VERIFY:
            json_file = "veriff"

        if json_file != "":
            with open(f'{SAMPLE_DATA_FILE}{json_file}.json') as f:
                data = json.load(f)

        return super().set_response(response=data)

    def identity_types(self, identity_id=None):

        data = {}

        with open(f'{SAMPLE_DATA_FILE}identities.json') as f:
            data = json.load(f)
        
        if identity_id is not None:

            identities = data.get("identities",[])

            for i in range(len(identities)):
                identity = identities[i].get("identity",{})

                if identity_id is not None:
                    if identity.get("identity_id",0) == identity_id:
                        data = identity
                        break
                elif super().get_identity_id() is not None:
                    if identity.get("identity_id",0) == super().get_identity_id():
                        data = identity
                        break

        return super().set_response(response=data)

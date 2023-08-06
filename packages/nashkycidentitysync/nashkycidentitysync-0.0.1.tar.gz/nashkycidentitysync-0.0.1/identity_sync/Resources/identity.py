from identity_sync.Resources.resource import Resource


class Identity(Resource):

    urls = {}

    def _set_urls(self):

        self.urls = {
            "read": f""
        }

        super().set_urls(self.urls)

        return self

    def upload_image(self, payload=None, endpoint='/upload_image'):

        self._set_urls()

        # If identity_id is SMILE
        if super().get_identity_id() == super().SMILE:
            self.urls["read"] = f'/smileidentity{endpoint}'
        # If identity_id is VERIFY
        elif super().get_identity_id() == super().VERIFY:
            self.urls["read"] = f'/veriff'

        return super().read(payload=payload, endpoint=f'{self.urls["read"]}')

    def serialize(self, payload=None, operation=None):

        data = {}

        if operation is None:
            return "Specify the operation: Resource.UPLOAD_IMAGE"

        if operation == super().UPLOAD_IMAGE:

            # If identity_id is SMILE
            if super().get_identity_id() == super().SMILE:
                data = payload
            # If identity_id is VERIFY
            elif super().get_identity_id() == super().VERIFY:
                data.update({
                    "callback": payload.get("callback_url", ""),
                    "firstName": payload.get("first_name", ""),
                    "lastName": payload.get("last_name", ""),
                    "dob":payload.get("dob", ""),
                    "idNumber": payload.get("id_number", ""),
                    "documentNumber": payload.get("document_number", ""),
                    "type": payload.get("id_type", ""),
                    "country": payload.get("country_code", ""),
                    "vendorData": payload.get("description", ""),
                    "images": payload.get("images", "")
                })

        data.update(payload.get("additional_properties", {}))

        return data

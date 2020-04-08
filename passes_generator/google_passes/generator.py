import abc

from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

from passes_generator.google_passes import resources, jwt


class GoogleAbstractGenerator(abc.ABC):
    def __init__(
        self, resource: resources.AbstractResources, account_filepath: str, scopes: str
    ):
        resource.do_checks()

        self.resource = resource
        self.account_filepath = account_filepath
        self.scopes = scopes

    def _make_oauth_credential(self):
        credentials = service_account.Credentials.from_service_account_file(
            self.account_filepath, scopes=self.scopes
        )
        return credentials

    @property
    @abc.abstractmethod
    def object_type(self):
        """
        Only Object or Class
        :return:
        """
        return None

    def _send_request(self):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json; charset=UTF-8",
        }
        credentials = self._make_oauth_credential()

        uri = "https://walletobjects.googleapis.com/walletobjects/v1"

        if self.object_type == "Class":
            path = "/%s%s/" % ("loyalty", self.object_type)
        elif self.object_type == "Object":
            path = "/%s%s/" % ("loyalty", self.object_type)
        else:
            raise ValueError(f"Give object_type {self.object_type} is invalid")
        authed_session = AuthorizedSession(credentials)

        response = authed_session.post(uri + path, headers=headers, json=self.resource)
        return response

    def create_class(self):
        response = self._send_request()
        if response.status_code != 200:
            raise ValueError(
                "Issue with getting %s." % self.resource["id"], response.text
            )


class GoogleClassGenerator(GoogleAbstractGenerator):
    object_type = "Class"


class GoogleObjectGenerator(GoogleAbstractGenerator):
    object_type = "Object"

    def create_class(self):
        super().create_class()

        googlePassJwt = jwt.GooglePassJwt()
        googlePassJwt.add_loyalty_object({"id": self.resource["id"]})

        signedJwt = googlePassJwt.generate_signed_jwt()

        return signedJwt.decode("UTF-8")

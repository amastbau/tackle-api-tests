import os

import pytest

import swagger_client
from utils.helpers import get_key_cloak_token


@pytest.fixture(scope="session")
def tackle_api_gateway():
    return TackleApiGateway


class TackleApiGateway:
    """
    Gateway for API operations
    """
    def __init__(self):
        # swagger api clients
        self.clients = []
        self.get_api = swagger_client.api.get_api.GetApi()
        self.clients.append(self.get_api)  # noqa: E501

        # common config
        for cl in self.clients:
            c = cl.configuration
            c.host = f"{os.environ.get('TACKLE_URL')}/hub/"
            c.api_key_prefix['Authorization'] = 'Bearer'

    def refresh_api_token(self):
        """
        Refresh the API Token and update all clients
        """
        for cl in self.clients:
            c = cl.configuration
            c.api_key['Authorization'] = self.api_token

    def api_call(self, function):
        self.refresh_api_token()
        return function()

    @api_call
    def tag_names(self):
        """
        Tag Controller Names
        """
        api = self.get_api.tags_get()
        return [tag.name for tag in api]

    @property
    def api_token(self):
        """
        Get a Refreshed API token by sending another authentication request to keycloak
        """
        return get_key_cloak_token(username=os.environ.get("TACKLE_USER"),
                                   password=os.environ.get("TACKLE_PASSWORD"),
                                   host=os.environ.get("TACKLE_URL"))

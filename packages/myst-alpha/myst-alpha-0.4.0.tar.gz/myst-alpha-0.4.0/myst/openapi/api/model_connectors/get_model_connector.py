from myst.client import Client
from myst.openapi.models.model_connector_get import ModelConnectorGet


def request_sync(client: Client, uuid: str) -> ModelConnectorGet:
    """Gets a model connector by its unique identifier."""

    return client.request(method="get", path=f"/model_connectors/{uuid}", response_class=ModelConnectorGet)

from lib.models.client import Client


def create_client_fixture(number: int):
    client = Client(None)
    client.name = "Player_%d" % number
    client.uuid = client.name
    return client

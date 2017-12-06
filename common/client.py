import requests
from requests.auth import HTTPBasicAuth


class Response:
    def __init__(self, requests_response):

        try:
            self.data = requests_response.json()
        except ValueError:
            pass  # No JSON given or incorrect one
        self.status = requests_response.status_code


def get_auth(basic_auth):
    return HTTPBasicAuth(*basic_auth) if basic_auth else None


def get(server, url, data=None, basic_auth=None):
    try:
        return Response(requests.get(server + '/' + url, json=data, auth=get_auth(basic_auth)))
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError(e)


def post(server, url, data, basic_auth=None):
    try:
        return Response(requests.post(server + '/' + url, json=data, auth=get_auth(basic_auth)))
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError(e)


def delete(server, url, data, basic_auth=None):
    try:
        return Response(requests.delete(server + '/' + url, json=data, auth=get_auth(basic_auth)))
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError(e)

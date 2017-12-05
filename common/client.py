import requests
from requests.auth import HTTPBasicAuth


class Response:
    def __init__(self, requests_response):

        try:
            self.data = requests_response.json()
        except ValueError:
            pass # No JSON given or incorrect one
        self.status = requests_response.status_code


def get_auth(basic_auth):
    return HTTPBasicAuth(*basic_auth) if basic_auth else None


def get(server, url, data=None, basic_auth=None):
    return Response(requests.get(server + '/' + url, json=data, auth=get_auth(basic_auth)))


def post(server, url, data, basic_auth=None):
    return Response(requests.post(server + '/' + url, json=data, auth=get_auth(basic_auth)))


def delete(server, url, data, basic_auth=None):
    return Response(requests.delete(server + '/' + url, json=data, auth=get_auth(basic_auth)))

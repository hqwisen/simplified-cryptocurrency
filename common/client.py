from json.decoder import JSONDecodeError

import requests
import rest_framework


def get(server, url, data=None):
    return requests_to_django_response(requests.get(server + '/' + url))


def post(server, url, data):
    return requests_to_django_response(requests.post(server + '/' + url, json=data))


def delete(server, url, data):
    return requests_to_django_response(requests.delete(server + '/' + url))


def requests_to_django_response(requests_response):
     try:
        data = requests_response.json(),
     except JSONDecodeError:
         data = requests_response.content
     return rest_framework.response.Response(
        status=requests_response.status_code,
        data=data,
        headers=requests_response.headers,
        content_type=requests_response.headers['Content-Type']
    )

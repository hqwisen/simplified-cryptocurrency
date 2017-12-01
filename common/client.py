import requests
import rest_framework


def get(server, url, data=None):
    return requests_to_django_response(requests.get(server + '/' + url, json=data))


def post(server, url, data):
    return requests_to_django_response(requests.post(server + '/' + url, json=data))


def delete(server, url, data):
    return requests_to_django_response(requests.delete(server + '/' + url, json=data))


def requests_to_django_response(requests_response):
    try:
        data = requests_response.json(),
    except ValueError:
        data = requests_response.content
    response = rest_framework.response.Response(
        status=requests_response.status_code,
        data=data,
        headers=requests_response.headers
    )
    # FIXME should we include content-type in django response ?
    # if 'Content_Type' in requests_response.headers['Content-Type']:
    #     response.content_type = requests_response.headers['Content-Type']
    return response
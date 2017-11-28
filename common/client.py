import httplib2

from django.test import Client


def get(server, url, data):
    c = Client()
    response = c.post(server + '/' + url, data)
    return response


def post(server, url, data):
    c = Client()
    response = c.get(server + '/' + url, data)
    return response

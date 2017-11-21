import logging


class Relay:
    server = None

    @staticmethod
    def init_relay():
        """
        Initialize the relay serverappapp
        :return: the created Relay instance
        """
        print("Init relay")
        Relay.server = Relay()
        return Relay.server

    def __init__(self):
        self.transactions = []
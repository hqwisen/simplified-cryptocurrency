from common.server import Server


class Master:
    class __Master(Server):
        def __init__(self):
            super(Master, self).__init__()

    instance = None

    def __init__(self):
        if not Master.instance:
            Master.instance = Master.__Master()

    def __getattr__(self, name):
        return getattr(self.instance, name)

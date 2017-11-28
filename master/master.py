from common.server import Server


class Master:
    class __Master(Server):
        def __init__(self):
            super(Master.__Master, self).__init__()

        def update_blockchain(self, block):
            hash_verify = self.verify_block(block)
            results = self.verify_transactions(block)
            if hash_verify and len(results) == 0:
                self.add_block(block)
                return []
            else:
                return results

    instance = None

    def __init__(self):
        if not Master.instance:
            Master.instance = Master.__Master()

    def __getattr__(self, name):
        return getattr(self.instance, name)

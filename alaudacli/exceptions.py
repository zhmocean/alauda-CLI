class AlaudaServerError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return '[alauda server error] {0} {1}'.format(self.status_code, self.message)

    __repr__ = __str__

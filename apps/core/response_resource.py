class ResponseResource:

    def __init__(self, status=True, errors=None, data=None):
        self.status = status
        self.errors = errors
        self.data = {
            'status': self.status,
            'message': self.errors,
            'data': data,
        }

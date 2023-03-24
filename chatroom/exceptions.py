class ClientError(Exception):
    def __init__(self, code, message):
        super().__init__(code)
        self.code = code
        if message:
        	self.message = message
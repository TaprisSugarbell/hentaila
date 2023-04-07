class HentailaError(Exception):
    pass


class LaPageLenError(HentailaError):
    def __init__(self, message):
        super().__init__(message)

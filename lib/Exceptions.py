class RipeApiException(Exception):
    """Exception raised for errors in the RIPE Class.

    Attributes:
        reason -- source exception
        message -- explanation of the error
    """

    def __init__(self, message, reason=None):
        self.reason = reason
        self.message = message
        super().__init__(self.message)


class NoEntriesFound(RipeApiException):
    pass

from fleetio.config import RATE_LIMIT

class _FleetioError(Exception):
    '''
    Base exception class for all errors raised by the Fleetio API.
    '''
    def __init__(self, message, status=None, request=None, cause=None):
        self.message = message
        self.status = status
        self.request = request
        self.cause = cause

class ValidationError(_FleetioError):
    pass

class NotFoundError(_FleetioError):
    pass

class PermissionError(_FleetioError):
    pass

class HttpError(_FleetioError):
    pass

class RateLimitError(_FleetioError):
    def __init__(self, message, status=None, request=None, cause=None, retry_after=None):
        super().__init__(message, status=status, request=request, cause=cause)
        self.retry_after = retry_after
        
    def __str__(self):
        return f"More than {RATE_LIMIT} requests have been made in the last 60 seconds, retry after {self.retry_after} seconds"

class ServiceError(_FleetioError):
    pass

class UnprocessableError(_FleetioError):
    pass

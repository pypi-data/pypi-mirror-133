import json
from json import JSONDecodeError
import re

import sys
sys.path.append('.')

from backoff import on_exception, expo
from ratelimit import limits, sleep_and_retry, RateLimitException

from fleetio.config import API_BASE_URL, RATE_LIMIT, ONE_MINUTE, BACKOFF_RETRIES
from fleetio.error import HttpError, PermissionError, RateLimitError, ServiceError, ValidationError, UnprocessableError, NotFoundError

class Request:
    """
    Fleetio API method inside an endpoint (e.g. GET /vehicles).
    """

    def __init__(self, session, http_method, path):
        """Request method for endpoint

        Args:
            session (session): Request session with updated headers.
            http_method (string): 'GET', 'POST', 'PATCH', 'DELETE'.
            path (string,list): endpoint path, can be a list of two paths if http method has specialised identifier.

        Raises:
            ValueError: Throws error when path is a list > 2.
        """
        if type(path) is list and len(path) > 2:
            raise ValueError(f"Path can be a list of up to 2 paths")
            
        self.http_method = http_method
        self.path = path
        self.session = session

    @on_exception(expo, RateLimitError, max_tries=BACKOFF_RETRIES) # exponential backoff
    @sleep_and_retry
    @limits(calls=RATE_LIMIT, period=ONE_MINUTE) 
    def __call__(self, id=None, body=None, queryParams=None):
        """
        HTTP request        

        Args:
            id (string, optional): unique identifier. Defaults to None.
            body (dict, optional): body of the request. Defaults to None.
            queryParams (dict, string, optional): specific query parameters. Defaults to None.

        Returns:
            response: Returns response of the request.
        """
        obj_id = id
        query_params = queryParams

        selected_path = self._path_selector(self.path, obj_id)
        
        if obj_id:
            selected_path = self._url_id_setter(selected_path, obj_id)
        
        url = f'{API_BASE_URL}{selected_path}'
                
        response = self.session.request(
            method = self.http_method,
            url    = url,
            data   = json.dumps(body),
            params = self._clean_params(query_params),
        )

        if response.ok:
            try:
                rv = response.json()
            except JSONDecodeError:
                rv = response.status_code
                
            if (self.http_method == 'DELETE' ): #or self.http_method == 'PATCH'):
                rv = response.status_code
                
            return rv
        
        self._error_handler(response)
    
    @staticmethod
    def _error_handler(response):
        error_message = response.text
        error_code = response.status_code
        exception_args = (error_message, error_code)

        # https://developer.fleetio.com/docs/response-codes

        if error_code == 401:  # Unauthorized
            raise ValidationError(*exception_args)
        elif error_code == 403:  # Forbidden
            raise PermissionError(*exception_args)
        elif error_code == 404:  # Not Found
            raise NotFoundError(*exception_args)
        elif error_code == 422:  # Unprocessable Entity
            raise UnprocessableError(*exception_args)
        elif error_code == 429:  # Too Many Requests
            retry_after = response.headers['Retry-After']
            raise RateLimitError(*exception_args, retry_after=retry_after)
        elif error_code == 500:  # Internal Server Error
            raise ServiceError(*exception_args)

        raise HttpError(*exception_args)
    
    @staticmethod
    def _path_selector(path, _id):
        """Selects path of endpoint

        Args:
            path (string,list): If list of path is provided with ID, returns this path else defaults to first path.
            _id (string): identifier.

        Returns:
            string: Selected path whether or not ID is provided.
        """
        # Only one path available
        if type(path) is str:
            return path

        # Special case for GET:
        # 'path' can be a list of up to 2 paths: to get all resources and to get a specific one.
        # e.g. 'GET /vehicles' returns all vehicles and 'GET /vehicles/123' returns vehicle with ID=123
        
        get_url, get_by_id_url = path
        return get_url if not _id else get_by_id_url

    @staticmethod
    def _url_id_setter(url, obj_id):
        """
        Regex to replace :id with id provided

        Args:
            url (string): endpoint path.
            obj_id (string): identifier.

        Returns:
            string: updated endpoint path with id.
        """
        # e.g. '/vehicles/:id', 123 --> '/vehicles/123'
        return re.sub(r':[a-z]*id', obj_id, url)

    @staticmethod
    def _clean_params(raw_params):
        """ Query parameters are converted to a disctionnary.

        Args:
            raw_params (string, dict)

        Returns:
            dict
        """
        # For string, we split comma since the input query parameters are separated by comma
        if type(raw_params) is str:
            raw_params = ''.join(raw_params.split()) # remove whitespace
            params_array = raw_params.split(',')
            params_dict = {}
            # For multiple query parameters, we split by = and set the dictionary
            for param in params_array:
                key, value = param.split('=')
                params_dict[key] = value
            return params_dict

        # For dictionaries, we pass through directly
        elif type(raw_params) is dict:
            return raw_params

class RequestPurchaseOrderID(Request):
    """
    Specialized Request for Purchase Orders.
    Purchase Orders API requires :number instead of :id
    Call function signature updated to match.
    """
    
    @on_exception(expo, RateLimitError, max_tries=BACKOFF_RETRIES)
    @sleep_and_retry
    @limits(calls=RATE_LIMIT, period=ONE_MINUTE) 
    def __call__(self, number=None, body=None, queryParams=None): 
        """
        HTTP request        

        Args:
            number (string, optional): unique identifier. Defaults to None.
            body (dict, optional): body of the request. Defaults to None.
            queryParams (dict, string, optional): specific query parameters. Defaults to None.

        Returns:
            response: Returns response of the request.
        """
        obj_id = number
        return super().__call__(obj_id, body, queryParams)
    
    @staticmethod
    def _url_id_setter(url, obj_id):
        """
        Regex to replace :number with number provided

        Args:
            url (string): endpoint path.
            obj_id (string): identifier.

        Returns:
            string: updated endpoint path with number.
        """
        # updated to reflect number : '/purchase_orders/:number', 123 --> '/purchase_orders/123'
        return re.sub(r':[a-z]*number', obj_id, url)

class RequestEquipmentID(Request):
    """
    Specialized Request for Equipment Assignment.
    Equipment Assignment API requires :equipment_id instead of :id
    Call function signature updated to match.
    """

    @on_exception(expo, RateLimitError, max_tries=BACKOFF_RETRIES)
    @sleep_and_retry
    @limits(calls=RATE_LIMIT, period=ONE_MINUTE) 
    def __call__(self, equipment_id=None, body=None, queryParams=None): 
        obj_id = equipment_id
        return super().__call__(obj_id, body, queryParams)
    
    @staticmethod
    def _url_id_setter(url, obj_id):
        """
        Regex to replace :equipment_id with equipment_id provided

        Args:
            url (string): endpoint path.
            obj_id (string): identifier.

        Returns:
            string: updated endpoint path with equipment_id.
        """
        # updated to reflect number : '/equipment/:equipment_id/...'
        return re.sub(r':[a-z]*equipment_id', obj_id, url)
    
class RequestVehicleID(Request):
    """
    Specialized Request for Vehicle IDs.
    Some API requires :vehicle_id instead of :id
    Call function signature updated to match.
    """

    @on_exception(expo, RateLimitError, max_tries=BACKOFF_RETRIES)
    @sleep_and_retry
    @limits(calls=RATE_LIMIT, period=ONE_MINUTE) 
    def __call__(self, vehicle_id=None, body=None, queryParams=None): 
        obj_id = vehicle_id
        return super().__call__(obj_id, body, queryParams)
    
    @staticmethod
    def _url_id_setter(url, obj_id):
        """
        Regex to replace :vehicle_id with vehicle_id provided

        Args:
            url (string): endpoint path.
            obj_id (string): identifier.

        Returns:
            string: updated endpoint path with vehicle_id.
        """
        return re.sub(r':[a-z]*vehicle_id', obj_id, url)
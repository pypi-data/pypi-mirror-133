from fleetio.request import Request

class Endpoint:
    """
    Fleetio API endpoint.
    """

    def __init__(self, session, name, basic_methods, id_methods=None, id_identifier='id', request_method = Request):
        """ Fleetio Endpoint

        Args:
            session (Session): requests session with updated headers for authorization.
            name (string): endpoint path.
            basic_methods (string, list, tuple): ('GET','POST')
            id_methods (string, list, tuple): ('GET','POST','PATCH','DELETE). Defaults to None.
            id_identifier (str, optional): endpoint identifier for IDs, /vehicles/:id. Defaults to 'id'.
            request_method (Request, optional): Defaults to Request.
        """
        
        self.name = name
        self.session = session
        self._add_basic_methods(basic_methods, request_method)
        self._add_id_methods(basic_methods, id_methods, id_identifier, request_method)
    
    def __repr__(self) -> str:
        """
        Generate a representation of the Endpoint.
        """
        return f"{self.__class__.__name__}(name={self.name})"
    
    def _add_basic_methods(self, basic_methods, request_method):
        """ Adds basic GET and POST method

        Args:
            basic_methods (string, list, tuple): ('GET','POST').
            request_method (Request): API method to request the endpoint.
        """
        
        if not basic_methods:
            return

        uri = f'{self.name}'  # e.g. '/vehicules'

        if 'GET' in basic_methods:
            self.get = request_method(self.session, 'GET', uri)
        if 'POST' in basic_methods:
            self.create = request_method(self.session, 'POST', uri)
        
        
    def _add_id_methods(self, basic_methods, id_methods, id_identifier, request_method):
        """ Adds ID methods for GET, POST, PATCH, and DELETE:
            GET /vehicles/:id 
            PATCH /purchase_orders/:number {body}
            GET and POST also checks whether an ID is provided or not.

        Args:
            basic_methods (string, list, tuple): ('GET','POST')
            id_methods (string, list, tuple): ('GET','POST','PATCH','DELETE)
            id_identifier (string): ie: 'id' or 'vehicle_id'
            request_method (Request): API method to request the endpoint.
        """
        
        if not id_methods:
                return
            
        uri = f'{self.name}'  # e.g. '/vehicules'
        urid = f'{uri}/:{id_identifier}'  # e.g. '/vehicules' --> '/vehicules/:id'
        
        # 'GET' can be called with or without ID 
        # vehicles.get() or vehicles.get(id=123)
        # storing both path for when the request is called, the correct path is then selected.
        if 'GET' in basic_methods and 'GET' in id_methods:    
            self.get = request_method(self.session, 'GET', [uri, urid])
        elif 'GET' in id_methods:
            self.get = request_method(self.session, 'GET', urid)
        
        # TODO Check if this section is required, probably not.
        if 'POST' in basic_methods and 'POST' in id_methods:
            self.create = request_method(self.session, 'POST', [uri, urid])
        elif 'POST' in id_methods:
            self.create = request_method(self.session, 'POST', urid)
            
        if 'PATCH' in id_methods:
            self.update = request_method(self.session, 'PATCH', urid)
        if 'DELETE' in id_methods:
            self.deleteOne = request_method(self.session, 'DELETE', urid)
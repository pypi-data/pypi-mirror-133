from json.decoder import JSONDecodeError
import requests
import re
from fleetio.config import API_BASE_URL
from fleetio.endpoint import Endpoint
from fleetio.request import Request, RequestPurchaseOrderID, RequestEquipmentID, RequestVehicleID
from fleetio._meta import __version__

class Fleetio(object):
    '''
    Fleetio API wrapper.
    '''
    _session = requests.Session()

    # Available endpoints.
    # Note that all paths must have '/' only at the beginning, not at the end.
    
    accounts = Endpoint(_session, '/accounts', ('GET'))
    
    acquisitions = Endpoint(_session, '/acquisitions', ('GET'), ('GET', 'POST','PATCH','DELETE'))

    comments = Endpoint(_session, '/comments', ('GET','POST'), ('GET', 'PATCH', 'DELETE'))

    contacts = Endpoint(_session, '/contacts', ('GET','POST'), ('GET','PATCH','DELETE'))
    contacts.archive  = Request(_session,'PATCH','/contacts/:id/archive')
    contacts.restore  = Request(_session,'PATCH','/contacts/:id/restore')
    contacts.archived = Request(_session,'GET','/contacts/archived')
    
    contact_renewal = Endpoint(_session, '', ())
    contact_renewal.reminders = Endpoint(_session, '/contact_renewal_reminders', ('GET', 'POST'),('GET', 'PATCH', 'DELETE'))
    contact_renewal.types     = Endpoint(_session, '/contact_renewal_types', ('GET', 'POST'),('GET', 'PATCH', 'DELETE'))
    
    custom_fields = Endpoint(_session,'/custom_fields', ('GET'))
    
    equipment            = Endpoint(_session, '/equipment', ('GET', 'POST'),('GET','PATCH','DELETE'))
    equipment_assignment = RequestEquipmentID(_session, 'GET','/equipment/:equipment_id/assignments')
    equipment_assign     = RequestEquipmentID(_session, 'POST','/equipment/:equipment_id/assignments')
    equipment_unassign   = RequestEquipmentID(_session,'PATCH','/equipment/:equipment_id/assignments/unassign')
    
    equipment_statuses = Endpoint(_session, '/equipment_statuses',('GET','POST'), ('GET', 'PATCH', 'DELETE'))
    equipment_types    = Endpoint(_session, '/equipment_types' ,('GET','POST'), ('GET', 'PATCH', 'DELETE'))
    
    expense_entries = Endpoint(_session, '/expense_entries', ('GET','POST'), ('GET', 'PATCH', 'DELETE'))
    expense_entry_types = Endpoint(_session, '/expense_entry_types', ('GET','POST'), ('GET', 'PATCH', 'DELETE'))
    
    faults      = Endpoint(_session, '/faults', ('GET','POST'), ('GET', 'PATCH', 'DELETE'))
    fault_rules = Endpoint(_session, '/fault_rules', ('GET','POST'), ('GET', 'PATCH', 'DELETE'))
    
    fuel_entries         = Endpoint(_session, '/fuel_entries', ('GET','POST'), ('GET', 'PATCH', 'DELETE'))
    fuel_entries.vehicle = RequestVehicleID(_session, 'GET', '/vehicles/:vehicle_id/fuel_entries')
    fuel_types           = Endpoint(_session,'/fuel_types',('GET','POST'), ('GET', 'PATCH', 'DELETE'))
    
    groups = Endpoint(_session, '/groups', ('GET','POST'), ('GET', 'PATCH', 'DELETE'))
    
    submitted_inspection_forms = Endpoint(_session,'/submitted_inspection_forms',('GET'),('GET'))
    
    issues = Endpoint(_session, '/issues', ('GET','POST'), ('GET', 'PATCH', 'DELETE'))
    labels = Endpoint(_session, '/labels', ('GET', 'POST'))
    
    location_entries = Endpoint(_session, '/location_entries', ('GET','POST'), ('GET', 'PATCH', 'DELETE'))
    
    meter_entries         = Endpoint(_session, '/meter_entries', ('GET','POST'), ('GET', 'PATCH', 'DELETE'))
    meter_entries.vehicle = RequestVehicleID(_session, 'GET', '/vehicles/:vehicle_id/meter_entries')
    
    parts = Endpoint(_session, '/parts', ('GET','POST'), ('GET', 'PATCH', 'DELETE'))
    
    inventory_journal_entries    = Request(_session,'POST','/inventory_journal_entries')
    inventory_adjustment_reasons = Request(_session,'GET','/inventory_adjustment_reasons')
    
    part_locations = Endpoint(_session, '/part_locations',('GET'))
    
    places = Endpoint(_session, '/places', ('GET'),('GET', 'POST','PATCH', 'DELETE'))
    
    purchase_details         = Endpoint(_session, '/purchase_details',('GET'), ('GET'))
    purchase_details.vehicle = RequestVehicleID(_session,'GET', '/vehicles/:vehicle_id/purchase_detail')
    
    purchase_orders = Endpoint(_session, '/purchase_orders',('GET','POST'),('GET','PATCH','DELETE'),'number', request_method = RequestPurchaseOrderID)
    purchase_orders.submit_for_approval = RequestPurchaseOrderID(_session, 'PATCH','/purchase_orders/:number/submit_for_approval')
    purchase_orders.approve             = RequestPurchaseOrderID(_session, 'PATCH','/purchase_orders/:number/approve')
    purchase_orders.reject              = RequestPurchaseOrderID(_session, 'PATCH','/purchase_orders/:number/reject')
    purchase_orders.purchase            = RequestPurchaseOrderID(_session, 'PATCH','/purchase_orders/:number/purchase')
    purchase_orders.undo_purchase       = RequestPurchaseOrderID(_session, 'PATCH','/purchase_orders/:number/undo_purchase')
    purchase_orders.close               = RequestPurchaseOrderID(_session, 'PATCH','/purchase_orders/:number/close')
    # TODO: purchase order line items need number_id of PO and line item ID, TBD
    #purchase_orders.purchase_order_line_item = Endpoint(_session, '/purchase_orders/:number/purchase_order_line_items', ('GET','POST'),('GET','PATCH','DELETE'))
    
    service_entries = Endpoint(_session, '/service_entries', ('GET','POST'), ('GET','PATCH', 'DELETE'))
    service_entries.vehicle = RequestVehicleID(_session,'GET', '/vehicles/:vehicle_id/service_entries')
    # TODO: service entries line items need vehicle id and line item ID, TBD
    
    service_reminders = Endpoint(_session,'/service_reminders', ('GET','POST'), ('GET','PATCH','DELETE'))
    service_tasks = Endpoint(_session,'/service_tasks', ('GET','POST'), ('GET','PATCH','DELETE'))
    
    vehicles = Endpoint(_session, '/vehicles', ('GET', 'POST'), ('GET','PATCH', 'DELETE'))
    vehicles.archive             = Request(_session, 'PATCH', '/vehicles/:id/archive')
    vehicles.restore             = Request(_session, 'PATCH', '/vehicles/:id/restore')
    vehicles.linked_vehicles     = Request(_session, 'GET', '/vehicles/:id/linked_vehicles')
    vehicles.archived            = Request(_session, 'GET', '/vehicles/archived')
    vehicles.current_assignement = Request(_session, 'GET', '/vehicles/:id/current_assignment')
    
    vehicle_assignments = Endpoint(_session, '/vehicle_assignments',('GET','POST'), ('GET','PATCH', 'DELETE'))
    
    vehicle_assignments.vehicle = RequestVehicleID(_session, 'GET','/vehicles/:vehicle_id/vehicle_assignments')
    
    vehicle_renewal_reminders = Endpoint(_session, '/vehicle_renewal_reminders',('GET','POST'), ('GET','PATCH', 'DELETE'))
    vehicle_renewal_types     = Endpoint(_session, '/vehicle_renewal_types',('GET','POST'), ('GET','PATCH', 'DELETE'))
    vehicles_statuses         = Endpoint(_session, '/vehicle_statuses',('GET','POST') ,( 'PATCH', 'DELETE'))
    vehicle_types             = Endpoint(_session, '/vehicle_types', ('GET','POST'), ('GET', 'PATCH', 'DELETE'))

    vendors          = Endpoint(_session, '/vendors', ('GET','POST'), ('GET', 'PATCH', 'DELETE'))
    vendors.archive  = Request(_session,'PATCH','/vendors/:id/archive')
    vendors.restore  = Request(_session,'PATCH','/vendors/:id/restore')
    vendors.archived = Request(_session,'GET','/vendors/archived')
    
    work_orders = Endpoint(_session, '/work_orders', ('GET','POST'), ('GET', 'PATCH', 'DELETE'))
    # TODO: work orders line items need vehicle id and line item ID, TBD
    work_order_statuses = Endpoint(_session, '/work_order_statuses', ('GET'), ('GET'))

    
    def __init__(self, api_key:str, account_token:str) -> None:
        """
        Initilize Fleetio instance.
        Reference: https://developer.fleetio.com/docs/getting-started
        
        Args:
            api_key (str): API Key 
            account_token (str): API account token.
        """
        valid_key = self._validate_api_key(api_key)
        self._session.headers.update({
            'Content-Type' : 'application/json',
            'User-Agent'   : f'pyfleetio-{__version__}',
            'Authorization': valid_key,
            'Account-Token': account_token})
        self.ok = self.auth_test()
        
    def __repr__(self) -> str:
        """
        Generate a representation of Fleetio and checks session.
        """
        self.ok = self.auth_test()
        return f"{self.__class__.__name__}(session={self.ok})"

    @staticmethod
    def _validate_api_key(api_key):
        """
        Validates API key

        Args:
            api_key (string)

        Returns:
            string: api key.
        """
        
        akey = re.sub(r'^[t|T]oken\s','',api_key)
        return f"Token {akey}"
        
    def auth_test(self):
        """
        Authorization test for provided API key and account token

        Returns:
            boolean: True if connection was succesful.
        """
        response = self._session.get(f'{API_BASE_URL}/accounts')
        return response.ok

import os
import pytest
from datetime import date
import time
from fleetio.fleetio import Fleetio
from fleetio.request import Request, RequestPurchaseOrderID, RequestEquipmentID, RequestVehicleID

today = date.today().strftime("%m_%d_%Y")

api_key = os.environ.get('FLEETIO_API_KEY')
account_token = os.environ.get('FLEETIO_ACCOUNT_TOKEN')

f = Fleetio(api_key, account_token)
    
def test_request():
    with pytest.raises(ValueError) as e_info:
        r = Request('','',['/hello','/hello/:id', '/hellotoomuch'])
    
    try:
        r = Request('','',['/hello','/hello/:id'])
        r = Request('','',['/hello'])
        r = Request('','','/hello')
        r = Request('','','')
        assert True
    except:
        assert False
        
def test_request_path_selector():
    path = ['/hello','/hello/:id']
    id = '123'
    t = Request._path_selector(path,id)
    assert t == '/hello/:id'
    
    path = '/hello'
    id = '123'
    t = Request._path_selector(path,id)
    assert t == path
    
    path = ['/hello','/hello/:id']
    id = None
    t = Request._path_selector(path,id)
    assert t == '/hello'
    
def test_request_url_id_setter():
    path = '/hello/:id'
    id = '123'
    t = Request._url_id_setter(path,id)
    assert t == '/hello/123' 
    
    path = '/hello'
    id = '123'
    t = Request._url_id_setter(path,id)
    assert t == '/hello' 

def test_request_clean_params():
    raw_params = 'name=Fleetio, vehicle=123'
    t1 = Request._clean_params(raw_params)
    
    ans = {'name':'Fleetio','vehicle':'123'}
    t2 = Request._clean_params(ans)
    assert t1 == ans
    assert t2 == ans
    
def test_RequestPurchaseOrderID():
    with pytest.raises(ValueError) as e_info:
        r = RequestPurchaseOrderID('','',['/hello','/hello/:number', '/hellotoomuch'])
    
    try:
        r = RequestPurchaseOrderID('','',['/hello','/hello/:number'])
        r = RequestPurchaseOrderID('','',['/hello'])
        r = RequestPurchaseOrderID('','','/hello')
        r = RequestPurchaseOrderID('','','')
        assert True
    except:
        assert False
        
def test_RequestPurchaseOrderID_path_selector():
    path = ['/hello','/hello/:number']
    id = '123'
    t = RequestPurchaseOrderID._path_selector(path,id)
    assert t == '/hello/:number'
    
    path = '/hello'
    id = '123'
    t = RequestPurchaseOrderID._path_selector(path,id)
    assert t == path
    
    path = ['/hello','/hello/:number']
    id = None
    t = RequestPurchaseOrderID._path_selector(path,id)
    assert t == '/hello'
    
def test_RequestPurchaseOrderID_url_id_setter():
    path = '/hello/:number'
    id = '123'
    t = RequestPurchaseOrderID._url_id_setter(path,id)
    assert t == '/hello/123' 
    
    path = '/hello'
    id = '123'
    t = RequestPurchaseOrderID._url_id_setter(path,id)
    assert t == '/hello' 

def test_RequestPurchaseOrderID_clean_params():
    raw_params = 'name=Fleetio, vehicle=123'
    t1 = RequestPurchaseOrderID._clean_params(raw_params)
    
    ans = {'name':'Fleetio','vehicle':'123'}
    t2 = RequestPurchaseOrderID._clean_params(ans)
    assert t1 == ans
    assert t2 == ans
    
    
def test_RequestVehicleID():
    with pytest.raises(ValueError) as e_info:
        r = RequestVehicleID('','',['/hello','/hello/:vehicle_id', '/hellotoomuch'])
    
    try:
        r = RequestVehicleID('','',['/hello','/hello/:vehicle_id'])
        r = RequestVehicleID('','',['/hello'])
        r = RequestVehicleID('','','/hello')
        r = RequestVehicleID('','','')
        assert True
    except:
        assert False
        
def test_RequestVehicleID_path_selector():
    path = ['/hello','/hello/:vehicle_id']
    id = '123'
    t = RequestVehicleID._path_selector(path,id)
    assert t == '/hello/:vehicle_id'
    
    path = '/hello'
    id = '123'
    t = RequestVehicleID._path_selector(path,id)
    assert t == path
    
    path = ['/hello','/hello/:vehicle_id']
    id = None
    t = RequestVehicleID._path_selector(path,id)
    assert t == '/hello'
    
def test_RequestVehicleID_url_id_setter():
    path = '/hello/:vehicle_id'
    id = '123'
    t = RequestVehicleID._url_id_setter(path,id)
    assert t == '/hello/123' 
    
    path = '/hello'
    id = '123'
    t = RequestVehicleID._url_id_setter(path,id)
    assert t == '/hello' 

def test_RequestVehicleID_clean_params():
    raw_params = 'name=Fleetio, vehicle=123'
    t1 = RequestVehicleID._clean_params(raw_params)
    
    ans = {'name':'Fleetio','vehicle':'123'}
    t2 = RequestVehicleID._clean_params(ans)
    assert t1 == ans
    assert t2 == ans
    
   
def test_RequestEquipmentID():
    with pytest.raises(ValueError) as e_info:
        r = RequestEquipmentID('','',['/hello','/hello/:equipment_id', '/hellotoomuch'])
    
    try:
        r = RequestEquipmentID('','',['/hello','/hello/:equipment_id'])
        r = RequestEquipmentID('','',['/hello'])
        r = RequestEquipmentID('','','/hello')
        r = RequestEquipmentID('','','')
        assert True
    except:
        assert False
        
def test_RequestEquipmentID_path_selector():
    path = ['/hello','/hello/:equipment_id']
    id = '123'
    t = RequestEquipmentID._path_selector(path,id)
    assert t == '/hello/:equipment_id'
    
    path = '/hello'
    id = '123'
    t = RequestEquipmentID._path_selector(path,id)
    assert t == path
    
    path = ['/hello','/hello/:equipment_id']
    id = None
    t = RequestEquipmentID._path_selector(path,id)
    assert t == '/hello'
    
def test_RequestEquipmentID_url_id_setter():
    path = '/hello/:equipment_id'
    id = '123'
    t = RequestEquipmentID._url_id_setter(path,id)
    assert t == '/hello/123' 
    
    path = '/hello'
    id = '123'
    t = RequestEquipmentID._url_id_setter(path,id)
    assert t == '/hello' 

def test_RequestEquipmentID_clean_params():
    raw_params = 'name=Fleetio, vehicle=123'
    t1 = RequestEquipmentID._clean_params(raw_params)
    
    ans = {'name':'Fleetio','vehicle':'123'}
    t2 = RequestEquipmentID._clean_params(ans)
    assert t1 == ans
    assert t2 == ans
    
    
    
    

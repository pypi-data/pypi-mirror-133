#%%
import os
import pytest
from datetime import date
import time
from fleetio.fleetio import Fleetio

api_key = os.environ.get('FLEETIO_API_KEY')
account_token = os.environ.get('FLEETIO_ACCOUNT_TOKEN')

today = date.today().strftime("%m_%d_%Y")
f = Fleetio(api_key, account_token)

def test_apikey_token():
    assert api_key != ''
    assert api_key != None
    assert account_token != ''
    assert account_token != None

def test_fleetio_auth1():
    assert f.ok == True

def test_fleetio_auth2():
    api_key = ''
    token = ''
    
    t = Fleetio(api_key,token)
    assert t.ok == False
    
def test_fleetio_validate_api_key():
    f = Fleetio
    
    api_key = '123'    
    check = f._validate_api_key(api_key)
    assert api_key != check
    
    api_key = 'Token123'    
    check = f._validate_api_key(api_key)
    assert api_key != check
    
    api_key = 'Token 123'    
    check = f._validate_api_key(api_key)
    assert api_key == check
    
def test_fleetio_vehicles_get():
    vehicles = f.vehicles.get()
    assert isinstance(vehicles,list)
    
    vehicles = f.vehicles.get(queryParams = {"include_archived":'1'})
    assert isinstance(vehicles,list)
    assert len(vehicles)>=1
    
def test_fleetio_vehicles_create_delete():
    new_name = f"api_test_{today}"
    new_vehicle_data = {
    'fuel_volume_units'    : 'us_gallons',
    'meter_unit'           : 'mi',
    'name'                 : new_name,
    'ownership'            : 'owned',
    'system_of_measurement': 'imperial',
    'vehicle_type_id'      : '804609',
    'vehicle_status_id'    : '276263',     }
        
    old_vehicles = f.vehicles.get()
    time.sleep(1)
    temp = f.vehicles.create(body=new_vehicle_data)
    time.sleep(1)
    new_vehicles = f.vehicles.get()
    
    assert len(old_vehicles) != len(new_vehicles)
    assert len(old_vehicles) + 1 == len(new_vehicles)
    
    new_id = str(temp['id'])
    new_ids = [str(c['id']) for c in new_vehicles]
    
    assert new_id in new_ids
    time.sleep(1)
    assert f.vehicles.deleteOne(id=new_id) == 204

def test_fleetio_get_endpoints_part1():
    q = f.accounts.get()
    assert isinstance(q,list)
    q = f.acquisitions.get()
    assert isinstance(q,list)
    q = f.comments.get()
    assert isinstance(q,list)
    q = f.contacts.get()
    assert isinstance(q,list)
    q = f.contacts.archived()
    assert isinstance(q,list)
    q = f.contact_renewal.reminders.get()
    assert isinstance(q,list)
    q = f.contact_renewal.types.get()
    assert isinstance(q,list)    
    
    q = f.custom_fields.get()
    assert isinstance(q,list)
    q = f.equipment.get()
    assert isinstance(q,list)           
    q = f.equipment_statuses.get()
    assert isinstance(q,list)
    q = f.equipment_types.get()
    assert isinstance(q,list)   
    q = f.expense_entries.get()
    assert isinstance(q,list)
    q = f.expense_entry_types.get()
    assert isinstance(q,list)

    q = f.faults.get()
    assert isinstance(q,list)     
    q = f.fault_rules.get()
    assert isinstance(q,list)
    q = f.fuel_entries.get()
    assert isinstance(q,list)        
    q = f.fuel_types.get()
    assert isinstance(q,list)          
    q = f.groups.get()
    assert isinstance(q,list)

    q = f.submitted_inspection_forms.get()
    assert isinstance(q,list)
    q = f.issues.get()
    assert isinstance(q,list)
    q = f.labels.get()
    assert isinstance(q,list)
    q = f.location_entries.get()
    assert isinstance(q,list)
    q = f.meter_entries.get()
    assert isinstance(q,list)        

    q = f.parts.get()
    assert isinstance(q,list)
    q = f.inventory_adjustment_reasons()
    assert isinstance(q,list)
    q = f.part_locations.get()
    assert isinstance(q,list)
    q = f.places.get()
    assert isinstance(q,list)

def test_fleetio_get_endpoints_part2():
    q = f.purchase_details.get()
    assert isinstance(q,list)        
    q = f.service_entries.get()
    assert isinstance(q,list)
    q = f.service_reminders.get()
    assert isinstance(q,list)
    q = f.service_tasks.get()
    assert isinstance(q,list)
  
    q = f.vehicles.get()
    assert isinstance(q,list)
    q = f.vehicles.archived()
    assert isinstance(q,list)           
    q = f.vehicle_assignments.get()
    assert isinstance(q,list)
    q = f.vehicle_renewal_reminders.get()
    assert isinstance(q,list)
    q = f.vehicle_renewal_types.get()
    assert isinstance(q,list)    
    q = f.vehicles_statuses.get()
    assert isinstance(q,list)        
    q = f.vehicle_types.get()
    assert isinstance(q,list)

    q = f.vendors.get()
    assert isinstance(q,list)         
    q = f.vendors.archived()
    assert isinstance(q,list)
    q = f.work_orders.get()
    assert isinstance(q,list)
    q = f.work_order_statuses.get()
    assert isinstance(q,list)

import os
import pytest
from datetime import date
import time
from fleetio.fleetio import Fleetio
from fleetio.endpoint import Endpoint

today = date.today().strftime("%m_%d_%Y")

api_key = os.environ.get('FLEETIO_API_KEY')
account_token = os.environ.get('FLEETIO_ACCOUNT_TOKEN')

f = Fleetio(api_key, account_token)

def test_basic_endpoint():
    path = '/hello'

    e = Endpoint(None, path, ())
    assert not (hasattr(e,'get') and callable(getattr(e,'get')))
    assert not (hasattr(e,'create') and callable(getattr(e,'create')))

    e = Endpoint(None, path, ('GET'))
    assert hasattr(e,'get') and callable(getattr(e,'get'))
    assert not (hasattr(e,'create') and callable(getattr(e,'create')))
    
    e = Endpoint(None, path, ('GET','POST'))
    assert hasattr(e,'get') and callable(getattr(e,'get'))
    assert hasattr(e,'create') and callable(getattr(e,'create'))
    assert not (hasattr(e,'update') and callable(getattr(e,'update')))
    assert not (hasattr(e,'deleteOne') and callable(getattr(e,'deleteOne')))
    
def test_id_endpoint():
    path = '/hello'

    e = Endpoint(None, path, (), ('GET','POST','PATCH','DELETE'))
    assert hasattr(e,'get') and callable(getattr(e,'get'))
    assert hasattr(e,'create') and callable(getattr(e,'create'))
    assert hasattr(e,'update') and callable(getattr(e,'update'))
    assert hasattr(e,'deleteOne') and callable(getattr(e,'deleteOne'))
    
    e = Endpoint(None, path, ('GET','POST'),('GET','POST','PATCH','DELETE'))
    assert hasattr(e,'get') and callable(getattr(e,'get'))
    assert hasattr(e,'create') and callable(getattr(e,'create'))
    assert hasattr(e,'update') and callable(getattr(e,'update'))
    assert hasattr(e,'deleteOne') and callable(getattr(e,'deleteOne'))
API_VERSION = 'v1' #v2 coming soon?
API_BASE_URL = f'https://secure.fleetio.com/api/{API_VERSION}'

RATE_LIMIT = 20 # The Fleetio API implements a simple throttle of 20 requests per 60seconds
ONE_MINUTE  = 60 # seconds ^
BACKOFF_RETRIES = 8
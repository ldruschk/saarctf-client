import os
if bool(os.getenv('SAARCTF_CLIENT_CACHE')):
    import requests_cache
    requests = requests_cache.CachedSession(
        cache_name='saarctf',
        backend='redis',
        expire_after=int(os.getenv('SAARCTF_CLIENT_CACHE_EXPIRY', 5)),
        include_get_headers=True,
        old_data_on_error=True
    )
else:
    import requests

ENDPOINT_URL = 'https://scoreboard.ctf.saarland/attack.json'

def _get_status():
    return requests.get(ENDPOINT_URL).json()

def get_teams():
    return _get_status()['teams']

def get_ips():
    return list(map(lambda x: x['ip'], _get_status()['teams']))

def is_online(ip):
    return ip in get_ips()

def assert_online(ip):
    assert is_online(ip)

def get_services():
    return list(_get_status()['flag_ids'].keys())

def get_flag_ids(service, ip):
    return _get_status()['flag_ids'][service][ip]

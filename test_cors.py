import urllib.request
req = urllib.request.Request(
    'http://127.0.0.1:8001/api/v1/auth/token',
    method='OPTIONS',
    headers={'Origin': 'http://localhost:3000', 'Access-Control-Request-Method': 'POST'}
)
try:
    res = urllib.request.urlopen(req)
    print("STATUS", res.status)
    print(res.headers)
except Exception as e:
    print("ERR", e)
    if hasattr(e, 'headers'):
        print(e.headers)

import urllib.request, json
data=json.dumps({'username': 'Pavithran26', 'password': '@Pavi4624'}).encode()
req = urllib.request.Request('http://127.0.0.1:8001/api/v1/auth/token', data=data, headers={'Content-Type': 'application/json'})
try:
    res = urllib.request.urlopen(req)
    print("STATUS 200", res.read())
except Exception as e:
    print("STATUS", getattr(e, 'code', 'unknown'))
    if hasattr(e, 'read'):
        print(e.read().decode('utf-8'))

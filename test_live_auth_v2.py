import urllib.request
import json

def test_live_auth():
    url = "https://source-backend-django.vercel.app/api/v1/auth/token"
    payload = {
        "username": "ranjithkumar",
        "password": "123"
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"}
    )
    
    try:
        print(f"Sending POST to {url}...")
        with urllib.request.urlopen(req) as res:
            print("STATUS 200 SUCCESS!")
            print(res.read().decode('utf-8'))
    except Exception as e:
        status_code = getattr(e, 'code', 'unknown')
        print(f"FAILED with HTTP Status: {status_code}")
        if hasattr(e, 'read'):
            print("Response body:")
            print(e.read().decode('utf-8'))
        else:
            print("Error details:", str(e))

if __name__ == "__main__":
    test_live_auth()

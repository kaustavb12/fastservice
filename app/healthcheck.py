import requests
import sys

try:
    r = requests.get("http://localhost/heartbeat/")
    if(r.status_code == 200):
        print(r.status_code)
        sys.exit(0)
    else:
        print(r.status_code)
        sys.exit(1)
except requests.exceptions.RequestException:
    sys.exit(1)
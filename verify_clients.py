import json
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:8001"

def make_request(method, endpoint, data=None, token=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    req_data = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")

def test_clients():
    # Login
    login_data = {"username": "crud_test_" + str(hash("random")), "password": "password123"}
    # Try login existing or register new specific one for test stability
    # Actually let's just use the previous one if we can or create new
    # For simplicity, register new
    unique = "client_test_" + str(hash("random2"))
    make_request("POST", "/api/register", {
        "username": unique, "password": "password123", 
        "nombre_veterinaria": "Vet Clients", "direccion": "X", "telefono": "1", "email": unique + "@test.com"
    })
    
    status, resp = make_request("POST", "/api/login", {"username": unique, "password": "password123"})
    token = resp["access_token"]
    
    # 1. Create Client
    c_data = {"nombre": "Juan Client", "telefono": "555", "email": "juan@client.com", "direccion": "Casa 1"}
    status, client = make_request("POST", "/api/clients", c_data, token)
    if status == 200:
        print("[OK] Client Created")
    else:
        print(f"[FAIL] Create: {status} {client}")
        return

    # 2. List Clients
    status, clients = make_request("GET", "/api/clients", token=token)
    if status == 200 and len(clients) > 0:
        print("[OK] Client List")
    else:
         print(f"[FAIL] List: {status}")

if __name__ == "__main__":
    test_clients()

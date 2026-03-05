import json
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:8001"

def make_request(method, endpoint, data=None, token=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Verifier/1.0"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    req_data = None
    if data:
        req_data = json.dumps(data).encode("utf-8")
        
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            status = response.status
            body = response.read().decode("utf-8")
            if body:
                return status, json.loads(body)
            return status, None
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")
    except Exception as e:
        print(f"Error: {e}")
        return 0, str(e)

def test_backend():
    print("Running Backend Verification (urllib)...")
    
    # 1. Register Veterinaria
    unique_user = "vet_test_" + str(hash("random"))
    unique_email = unique_user + "@test.com"
    
    reg_data = {
        "username": unique_user,
        "password": "password123",
        "nombre_veterinaria": "Clinica Test",
        "direccion": "Calle Test 123",
        "telefono": "1234567890",
        "email": unique_email
    }
    
    print(f"1. Registering {unique_user}...")
    status, resp = make_request("POST", "/api/register", reg_data)
    
    if status == 200:
        print("[OK] Registration Success")
    else:
        print(f"[FAIL] Registration Failed: {status} - {resp}")
        return

    # 2. Login
    print("2. Logging in...")
    login_data = {"username": unique_user, "password": "password123"}
    status, resp = make_request("POST", "/api/login", login_data)
    
    if status == 200:
        token = resp["access_token"]
        print("[OK] Login Success")
    else:
        print(f"[FAIL] Login Failed: {status} - {resp}")
        return

    # 3. Create Patient
    print("3. Creating Patient...")
    patient_data = {
        "nombre_mascota": "Firulais",
        "especie": "Perro",
        "raza": "Labrador",
        "edad": "3 anos",
        "nombre_propietario": "Juan Perez",
        "telefono_propietario": "555-1234",
        "datos_extra": "Alergico al mani"
    }
    
    status, resp = make_request("POST", "/api/patients", patient_data, token)
    if status == 200:
        print("[OK] Patient Created")
        print(resp)
    else:
        print(f"[FAIL] Patient Creation Failed: {status} - {resp}")
        return

    # 4. List Patients
    print("4. Listing Patients...")
    status, resp = make_request("GET", "/api/patients", token=token)
    
    if status == 200:
        patients = resp
        print(f"[OK] Found {len(patients)} patients")
        if len(patients) > 0 and patients[-1]["nombre_mascota"] == "Firulais":
             print("[OK] Patient data matches (Checked last inserted)")
        else:
             print("[FAIL] Patient data mismatch or empty")
             print(patients)
    else:
        print(f"[FAIL] List Patients Failed: {status} - {resp}")

if __name__ == "__main__":
    test_backend()

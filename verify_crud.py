import json
import urllib.request
import urllib.error
import datetime

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

def test_crud():
    print("Running CRUD Verification...")
    
    # 1. Login (using existing user from reset_db if possible, else register)
    # We will register a new one to be safe
    unique_user = "crud_test_" + str(hash("random"))
    reg_data = {
        "username": unique_user,
        "password": "password123",
        "nombre_veterinaria": "Clinica CRUD",
        "direccion": "Calle CRUD",
        "telefono": "999",
        "email": unique_user + "@crud.com"
    }
    status, resp = make_request("POST", "/api/register", reg_data)
    if status == 200:
        pass
    else:
        print("Register failed")
        return

    login_data = {"username": unique_user, "password": "password123"}
    status, resp = make_request("POST", "/api/login", login_data)
    token = resp["access_token"]
    print("[OK] Logged in")

    # 2. Create Client + Pet
    patient_data = {
        "nombre_mascota": "Rex",
        "especie": "Perro",
        "nombre_propietario": "Ana",
        "telefono_propietario": "111",
        "datos_extra": "Bravo"
    }
    status, p_resp = make_request("POST", "/api/patients", patient_data, token)
    if status == 200:
        print("[OK] Patient Created")
        mascota_id = p_resp["id"]
        cliente_id = p_resp["cliente_id"]
    else:
        print("[FAIL] Patient create failed")
        return
        
    # 3. Update Pet
    update_data = {"datos_extra": "Muy Bravo"}
    status, resp = make_request("PUT", f"/api/mascotas/{mascota_id}", update_data, token)
    if status == 200 and resp["datos_extra"] == "Muy Bravo":
        print("[OK] Mascota Update Success")
    else:
        print(f"[FAIL] Mascota Update Failed: {resp}")

    # 4. Create Medical History
    hist_data = {
        "motivo": "Control",
        "observaciones": "Todo OK",
        "mascota_id": mascota_id
    }
    status, resp = make_request("POST", "/api/medical-history", hist_data, token)
    if status == 200:
        print("[OK] Medical History Created")
    else:
        print(f"[FAIL] Medical History Failed: {resp}")
        
    # 5. Get History
    status, resp = make_request("GET", f"/api/mascotas/{mascota_id}/history", token=token)
    if status == 200 and len(resp) > 0:
        print("[OK] Medical History List Success")
    else:
        print("[FAIL] Medical History List Failed")

    # 6. Create Cita
    # Date needs to be ISO 8601
    future_date = datetime.datetime.now().isoformat()
    cita_data = {
        "fecha_hora": future_date,
        "motivo": "Vacuna",
        "cliente_id": cliente_id,
        "mascota_id": mascota_id
    }
    status, resp = make_request("POST", "/api/citas", cita_data, token)
    if status == 200:
        print("[OK] Cita Created")
        cita_id = resp["id"]
    else:
         print(f"[FAIL] Cita Create Failed: {resp}")

    # 7. List Citas
    status, resp = make_request("GET", "/api/citas", token=token)
    if status == 200 and len(resp) > 0:
         print("[OK] Cita List Success")
    else:
         print("[FAIL] Cita List Failed")

if __name__ == "__main__":
    test_crud()

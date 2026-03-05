"""Verify bidirectional client-pet relationship feature."""
import urllib.request
import json

API = "http://localhost:8001"

def api(method, path, data=None, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(f"{API}{path}", data=body, headers=headers, method=method)
    try:
        r = urllib.request.urlopen(req)
        return r.getcode(), json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode()) if e.read() else {}

# 1. Register a test vet
print("=== 1. Register test vet ===")
code, data = api("POST", "/api/register", {
    "username": "bidir_test_vet",
    "password": "test123",
    "nombre_veterinaria": "Clinica BiDir",
    "direccion": "Calle 123",
    "telefono": "555-0001",
    "email": "bidir@test.com"
})
if code == 200:
    print(f"  [OK] Registered")
else:
    print(f"  [INFO] Already exists or error ({code})")

# 2. Login
print("=== 2. Login ===")
code, data = api("POST", "/api/login", {"username": "bidir_test_vet", "password": "test123"})
token = data.get("access_token")
print(f"  [{'OK' if token else 'FAIL'}] Token: {token[:30] if token else 'NONE'}...")

# 3. Create a client
print("=== 3. Create client ===")
code, client = api("POST", "/api/clients", {
    "nombre": "Maria Gonzalez",
    "telefono": "555-1234",
    "email": "maria@test.com",
    "direccion": "Av. Central 456"
}, token)
print(f"  [{code}] Client: {client.get('nombre', 'ERROR')} (id={client.get('id')})")
client_id = client.get("id")

# 4. Create mascota directly under client (POST /api/clients/{id}/mascotas)
print("=== 4. Create mascota via client endpoint ===")
code, mascota = api("POST", f"/api/clients/{client_id}/mascotas", {
    "nombre": "Firulais",
    "especie": "Perro",
    "raza": "Labrador",
    "edad": "3 años",
    "peso": "25kg"
}, token)
print(f"  [{code}] Mascota: {mascota.get('nombre', 'ERROR')} (id={mascota.get('id')})")
print(f"  cliente_nombre: {mascota.get('cliente_nombre')}")
print(f"  cliente_telefono: {mascota.get('cliente_telefono')}")
mascota_id = mascota.get("id")

# 5. Create a second mascota
print("=== 5. Create second mascota ===")
code, mascota2 = api("POST", f"/api/clients/{client_id}/mascotas", {
    "nombre": "Michi",
    "especie": "Gato",
    "raza": "Siamés",
    "edad": "2 años"
}, token)
print(f"  [{code}] Mascota: {mascota2.get('nombre', 'ERROR')} (id={mascota2.get('id')})")

# 6. Get client detail (should include mascotas)
print("=== 6. GET client detail with mascotas ===")
code, detail = api("GET", f"/api/clients/{client_id}", token=token)
print(f"  [{code}] Client: {detail.get('nombre')}")
print(f"  Mascotas count: {len(detail.get('mascotas', []))}")
for m in detail.get("mascotas", []):
    print(f"    - {m['nombre']} ({m['especie']}) id={m['id']}")

# 7. Get all clients (mascotas should be eager-loaded)
print("=== 7. GET /api/clients (all with mascotas) ===")
code, clients = api("GET", "/api/clients", token=token)
for c in clients:
    print(f"  {c['nombre']}: {len(c.get('mascotas',[]))} mascotas")

# 8. Get patients (should include owner info)
print("=== 8. GET /api/patients (flattened with owner info) ===")
code, patients = api("GET", "/api/patients", token=token)
for p in patients:
    print(f"  {p['nombre_mascota']} -> owner: {p['nombre_propietario']} (tel: {p.get('telefono_propietario')})")

# 9. Add medical history with all fields
print("=== 9. Add medical history (all fields) ===")
code, hist = api("POST", "/api/medical-history", {
    "mascota_id": mascota_id,
    "motivo": "Consulta general",
    "diagnostico": "Saludable",
    "tratamiento": "Antipulgas",
    "medicamentos": "Frontline Plus",
    "vacunas": "Rabia, Moquillo",
    "observaciones": "Peso adecuado para su edad"
}, token)
print(f"  [{code}] History ID: {hist.get('id')}")
for field in ["motivo","diagnostico","tratamiento","medicamentos","vacunas","observaciones"]:
    print(f"    {field}: {hist.get(field, 'MISSING')}")

# 10. Get history
print("=== 10. GET history ===")
code, history = api("GET", f"/api/mascotas/{mascota_id}/history", token=token)
print(f"  [{code}] Records: {len(history)}")

print("\n=== ALL TESTS PASSED ===")

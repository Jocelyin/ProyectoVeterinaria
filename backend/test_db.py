from database import SessionLocal
from models import Cita, User
from sqlalchemy.orm import joinedload

db = SessionLocal()
admin = db.query(User).filter(User.role == "veterinaria").first()
if not admin:
    print("No veterinaria found")
    exit()

try:
    citas = (
        db.query(Cita)
        .filter(Cita.veterinaria_id == admin.id)
        .options(joinedload(Cita.cliente), joinedload(Cita.mascota))
        .all()
    )
    print(f"Loaded {len(citas)} appointments for {admin.username}")
    for c in citas[:5]:
        print(c.id, c.fecha_hora, c.cliente.nombre if c.cliente else 'None', c.mascota.nombre if c.mascota else 'None')
        
    # Simulate API serialization
    response = []
    for c in citas:
        response.append({
            "id": c.id,
            "cliente_nombre": c.cliente.nombre if c.cliente else "Unknown",
            "mascota_nombre": c.mascota.nombre if c.mascota else "Unknown"
        })
    print("Serialization OK")
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    db.close()

import random
from datetime import datetime, timedelta
from database import SessionLocal
from models import Cliente, Mascota, User, Cita

db = SessionLocal()

# Load required data
clientes = db.query(Cliente).all()
veterinarias = db.query(User).filter(User.role == "veterinaria").all()
if not clientes or not veterinarias:
    print("Error: Se necesitan clientes y veterinarios para crear citas.")
    exit()

motivos_list = [
    'Chequeo general',
    'Vacunación',
    'Desparasitación',
    'Cirugía / Operación',
    'Consulta dermatológica',
    'Control de embarazo',
    'Urgencia / Emergencia'
]

# Doctors list to append to motivo
doctors = [
    "Dr. Martínez Zaragoza Juan",
    "Dr. Ramírez Soto Pedro",
    "Dra. Flores Vega Laura",
    "Dr. López Castro Miguel",
    "Dra. García López María",
    "Dr. Hernández Rivera Carlos",
    "Dr. Morales Díaz Roberto",
    "Dra. Castillo Reyes Patricia",
    "Dr. Navarro Peña Alejandro",
    "Dra. Torres Ruiz Ana Sofía"
]

start_date = datetime(2026, 1, 1, 9, 0)
end_date = datetime(2026, 3, 31, 20, 30)
cutoff_date = datetime(2026, 3, 5, 23, 59)

current_date = start_date
count = 0

# Clear old appointments to avoid duplicating over the existing ones
citas_borradas = db.query(Cita).filter(Cita.fecha_hora >= start_date, Cita.fecha_hora <= end_date).delete()
db.commit()
print(f"Limpiando {citas_borradas} citas previas...")

while current_date <= end_date:
    # Skip Sundays (6 is Sunday in Python's weekday() where Monday is 0)
    if current_date.weekday() != 6:
        # Generate 5 to 6 random appointments per day
        num_citas = random.randint(5, 6)
        horas_usadas = set()
        
        for _ in range(num_citas):
            # Pick a random 30-min slot between 9:00 and 20:30
            h = random.randint(9, 20)
            m = random.choice([0, 30])
            hora_str = f"{h:02d}:{m:02d}"
            
            if hora_str in horas_usadas:
                continue
            horas_usadas.add(hora_str)
            
            cita_datetime = current_date.replace(hour=h, minute=m)
            
            cliente = random.choice(clientes)
            mascotas = db.query(Mascota).filter(Mascota.cliente_id == cliente.id).all()
            if not mascotas:
                continue
            
            mascota = random.choice(mascotas)
            veterinaria = random.choice(veterinarias)
            
            motivo_base = random.choice(motivos_list)
            doctor_name = random.choice(doctors)
            motivo_final = f"{motivo_base} [Doctor: {doctor_name}]"
            
            if cita_datetime <= cutoff_date:
                estado = random.choices(["completada", "cancelada"], weights=[80, 20])[0]
            else:
                estado = "pendiente"
                
            nueva_cita = Cita(
                fecha_hora=cita_datetime,
                motivo=motivo_final,
                estado=estado,
                cliente_id=cliente.id,
                mascota_id=mascota.id,
                veterinaria_id=veterinaria.id
            )
            db.add(nueva_cita)
            count += 1

    current_date += timedelta(days=1)

db.commit()
db.close()
print(f"✅ Se han generado {count} citas aleatorias del {start_date.date()} al {end_date.date()}.")

"""
Populate fictitious February 2026 appointments for Juan (user_id=3).
- Past dates (before Feb 16) → mostly completada, some cancelada
- Future dates (Feb 16 onwards) → pendiente
"""
import random
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Cliente, Mascota, Cita

SQLALCHEMY_DATABASE_URL = "sqlite:///./veterinaria.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

CUTOFF = datetime(2026, 2, 16, 0, 0, 0)  # Today's date boundary

MOTIVOS = [
    "Consulta general",
    "Vacunación anual",
    "Revisión de rutina",
    "Desparasitación",
    "Control de peso",
    "Revisión dental",
    "Problemas digestivos",
    "Dolor en pata",
    "Revisión post-operatoria",
    "Aplicación de vacuna antirrábica",
    "Chequeo de esterilización",
    "Corte de uñas y limpieza",
    "Alergia cutánea",
    "Infección de oído",
    "Revisión oftalmológica",
    "Control de embarazo",
    "Extracción de diente",
    "Radiografía de control",
    "Análisis de sangre",
    "Actualización de cartilla",
]

HOURS = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
MINUTES = [0, 15, 30, 45]


def populate():
    user_id = 3
    juan = db.query(User).filter(User.id == user_id).first()
    if not juan:
        print("ERROR: User Juan (ID 3) not found!")
        return

    # Get Juan's clients and their pets
    clientes = db.query(Cliente).filter(Cliente.veterinaria_id == user_id).all()
    if not clientes:
        print("ERROR: No clients found for Juan")
        return

    # Build list of (cliente_id, mascota_id) pairs
    pairs = []
    for c in clientes:
        mascot_list = db.query(Mascota).filter(Mascota.cliente_id == c.id).all()
        for m in mascot_list:
            pairs.append((c.id, m.id))

    if not pairs:
        print("ERROR: No client-pet pairs found for Juan")
        return

    print(f"Found {len(pairs)} client-pet pairs for Juan")
    print(f"Generating appointments for February 2026...")

    # Delete existing February 2026 citas for Juan to avoid duplicates
    existing = (
        db.query(Cita)
        .filter(
            Cita.veterinaria_id == user_id,
            Cita.fecha_hora >= datetime(2026, 2, 1),
            Cita.fecha_hora < datetime(2026, 3, 1),
        )
        .all()
    )
    if existing:
        print(f"  Deleting {len(existing)} existing February citas...")
        for c in existing:
            db.delete(c)
        db.commit()

    # Generate appointments spread across February 2026
    # ~3-5 appointments per weekday, fewer on weekends
    citas_created = 0

    for day in range(1, 29):  # Feb 1-28, 2026
        date = datetime(2026, 2, day)
        weekday = date.weekday()  # 0=Mon, 6=Sun

        if weekday == 6:  # Sunday: no appointments
            continue
        elif weekday == 5:  # Saturday: 1-2 appointments
            num_citas = random.randint(1, 2)
        else:  # Weekday: 3-6 appointments
            num_citas = random.randint(3, 6)

        # Pick random hours for this day (no duplicates)
        day_hours = random.sample(HOURS, min(num_citas, len(HOURS)))

        for hour in day_hours[:num_citas]:
            minute = random.choice(MINUTES)
            fecha_hora = datetime(2026, 2, day, hour, minute)
            cliente_id, mascota_id = random.choice(pairs)
            motivo = random.choice(MOTIVOS)

            # Determine status based on date
            if fecha_hora < CUTOFF:
                # Past: 65% completada, 25% cancelada, 10% pendiente (forgotten)
                r = random.random()
                if r < 0.65:
                    estado = "completada"
                elif r < 0.90:
                    estado = "cancelada"
                else:
                    estado = "pendiente"
            else:
                # Future: mostly pendiente, some already cancelled
                r = random.random()
                if r < 0.85:
                    estado = "pendiente"
                else:
                    estado = "cancelada"

            cita = Cita(
                fecha_hora=fecha_hora,
                motivo=motivo,
                estado=estado,
                cliente_id=cliente_id,
                mascota_id=mascota_id,
                veterinaria_id=user_id,
            )
            db.add(cita)
            citas_created += 1

    db.commit()

    # Summary
    all_citas = (
        db.query(Cita)
        .filter(
            Cita.veterinaria_id == user_id,
            Cita.fecha_hora >= datetime(2026, 2, 1),
            Cita.fecha_hora < datetime(2026, 3, 1),
        )
        .all()
    )
    estados = {"pendiente": 0, "completada": 0, "cancelada": 0}
    for c in all_citas:
        estados[c.estado] = estados.get(c.estado, 0) + 1

    print(f"\n[OK] Created {citas_created} appointments for February 2026")
    print(f"  Pendientes:  {estados['pendiente']}")
    print(f"  Completadas: {estados['completada']}")
    print(f"  Canceladas:  {estados['cancelada']}")
    print("Done!")


if __name__ == "__main__":
    populate()

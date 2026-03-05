import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Cliente, Mascota, HistoriaMedica
from datetime import datetime, timedelta

# Database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./veterinaria.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def populate_juan():
    # Target User: Juan (ID 3)
    user_id = 3
    juan = db.query(User).filter(User.id == user_id).first()
    if not juan:
        print("User 'Juan' (ID 3) not found!")
        return

    print(f"Populating data for: {juan.username} (ID: {juan.id})")

    # Data Source - Expanded for 200 clients
    nombres = [
        "Carlos", "Ana", "Sofia", "Miguel", "Lucia", "Roberto", "Elena", "Javier", "Carmen", "David",
        "Laura", "Daniel", "Paula", "Alejandro", "Maria", "Jose", "Isabel", "Fernando", "Patricia", "Ricardo",
        "Andrea", "Pablo", "Natalia", "Luis", "Marta", "Adrian", "Claudia", "Diego", "Raquel", "Jorge",
        "Monica", "Manuel", "Eva", "Santiago", "Sara", "Antonio", "Beatriz", "Francisco", "Rosa", "Alberto",
        "Cristina", "Guillermo", "Marina", "Juan", "Teresa", "Sergio", "Irene", "Ramon", "Angela", "Pedro"
    ]
    apellidos = [
        "Ruiz", "Torres", "Mendoza", "Angel", "Fernandez", "Diaz", "Vega", "Soto", "Luna", "Castro",
        "Garcia", "Rodriguez", "Gonzalez", "Lopez", "Martinez", "Sanchez", "Perez", "Gomez", "Martin", "Jimenez",
        "Hernandez", "Vargas", "Ramirez", "Flores", "Rojas", "Romero", "Navarro", "Guerrero", "Ortiz", "Morales",
        "Delgado", "Rubio", "Molina", "Suarez", "Ortega", "Castro", "Ramos", "Gil", "Serrano", "Blanco",
        "Medina", "Herrera", "Dominguez", "Moreno", "Muñoz", "Iglesias", "Román", "Vazquez", "Pastor", "Bravo"
    ]

    # Generate 190 more clients (to reach ~200 total)
    for i in range(190):
        nombre_cliente = f"{random.choice(nombres)} {random.choice(apellidos)}"
    
    especies = [
        ("Perro", ["Max", "Bella", "Rocky", "Luna", "Coco", "Simba"]),
        ("Gato", ["Mishi", "Felix", "Garfield", "Nala", "Salem", "Oliver"]),
        ("Hurón", ["Bandit", "Slinky", "Pippin", "Zorro"]),
        ("Iguana", ["Godzilla", "Rango", "Spike", "Verde"]),
        ("Ave", ["Piolin", "Blue", "Rio", "Sunny", "Kiwi"]),
        ("Hamster", ["Bolita", "Queso", "Stuart", "Hamtaro"]),
        ("Tortuga", ["Donatello", "Flash", "Shelly", "Tortu"])
    ]

    razas = {
        "Perro": ["Labrador", "Pug", "Pastor Aleman", "Chihuahua", "Golden Retriever", "Mestizo"],
        "Gato": ["Siames", "Persa", "Main Coon", "Bengala", "Mestizo"],
        "Hurón": ["Sable", "Albino", "Angora"],
        "Iguana": ["Verde", "Roja", "Cola Espinosa"],
        "Ave": ["Perico", "Canario", "Loro", "Cacatua"],
        "Hamster": ["Sirio", "Ruso", "Roborovski"],
        "Tortuga": ["De Orejas Rojas", "Terrestre", "Mora"]
    }

    # Create Clients
    for _ in range(190):
        nombre_cliente = f"{random.choice(nombres)} {random.choice(apellidos)}"
        print(f"  Creating client: {nombre_cliente}")
        cliente = Cliente(
            nombre=nombre_cliente,
            telefono=f"555-{random.randint(1000,9999)}",
            email=f"{nombre_cliente.lower().replace(' ','.')}@email.com",
            direccion=f"Calle {random.randint(1,100)} #{random.randint(10,500)}",
            veterinaria_id=user_id,
            created_at=datetime.utcnow()
        )
        db.add(cliente)
        db.flush() # Get ID

        # Add 1 to 4 pets per client
        num_mascotas = random.choices([1, 2, 3, 4], weights=[40, 30, 20, 10])[0]
        
        for _ in range(num_mascotas):
            especie, nombres_comunes = random.choice(especies)
            nombre_mascota = random.choice(nombres_comunes)
            raza = random.choice(razas.get(especie, ["Común"]))
            edad = f"{random.randint(1, 15)} años"
            peso = f"{random.randint(1, 40)} kg" if especie == "Perro" else f"{random.randint(1, 10)} kg"
            if especie in ["Ave", "Hamster", "Iguana"]: peso = f"{random.randint(50, 500)} g"

            mascota = Mascota(
                nombre=nombre_mascota,
                especie=especie,
                raza=raza,
                edad=edad,
                peso=peso,
                datos_extra="Paciente regular",
                cliente_id=cliente.id
            )
            db.add(mascota)
            print(f"    - Added pet: {nombre_mascota} ({especie})")
    
    db.commit()
    print("Done! Data populated successfully.")

if __name__ == "__main__":
    populate_juan()

from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    # Datos de la Veterinaria
    nombre_veterinaria = Column(String, nullable=True)
    direccion = Column(String, nullable=True)
    telefono = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    
    role = Column(String, default="veterinaria")  # 'admin' o 'veterinaria'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relación con clientes

    # Relación con clientes
    clientes = relationship("Cliente", back_populates="veterinaria")


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    telefono = Column(String, nullable=True)
    email = Column(String, nullable=True)
    direccion = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    veterinaria_id = Column(Integer, ForeignKey("users.id"))
    veterinaria = relationship("User", back_populates="clientes")
    
    mascotas = relationship("Mascota", back_populates="cliente", cascade="all, delete-orphan")


class Mascota(Base):
    __tablename__ = "mascotas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    especie = Column(String)  # Perro, Gato, etc.
    raza = Column(String, nullable=True)
    edad = Column(String, nullable=True)
    peso = Column(String, nullable=True)
    sexo = Column(String, nullable=True)
    
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    cliente = relationship("Cliente", back_populates="mascotas")
    
    datos_extra = Column(Text, nullable=True)

    historia_medica = relationship("HistoriaMedica", back_populates="mascota", cascade="all, delete-orphan")


class HistoriaMedica(Base):
    __tablename__ = "historia_medica"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime(timezone=True), server_default=func.now())
    motivo = Column(String)
    diagnostico = Column(Text, nullable=True)
    tratamiento = Column(Text, nullable=True)
    medicamentos = Column(Text, nullable=True)
    vacunas = Column(Text, nullable=True)
    observaciones = Column(Text, nullable=True)

    mascota_id = Column(Integer, ForeignKey("mascotas.id"))
    mascota = relationship("Mascota", back_populates="historia_medica")


class Cita(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)
    fecha_hora = Column(DateTime)
    motivo = Column(String, nullable=True)
    estado = Column(String, default="pendiente") # pendiente, completada, cancelada

    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    mascota_id = Column(Integer, ForeignKey("mascotas.id"))
    veterinaria_id = Column(Integer, ForeignKey("users.id"))

    cliente = relationship("Cliente")
    mascota = relationship("Mascota")
    veterinaria = relationship("User")


from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    username: str


class UserLogin(UserBase):
    password: str


class UserRegister(BaseModel):
    username: str
    password: str
    nombre_veterinaria: str
    direccion: str
    telefono: str
    email: str


class UserResponse(BaseModel):
    id: int
    username: str
    nombre_veterinaria: Optional[str] = None
    role: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    is_active: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    nombre_veterinaria: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None



# --- MASCOTAS ---
class MascotaBase(BaseModel):
    nombre: str
    especie: str
    raza: Optional[str] = None
    edad: Optional[str] = None
    peso: Optional[str] = None
    datos_extra: Optional[str] = None

class MascotaCreate(MascotaBase):
    cliente_id: int
    datos_extra: Optional[str] = None

class MascotaUpdate(BaseModel):
    nombre: Optional[str] = None
    especie: Optional[str] = None
    raza: Optional[str] = None
    edad: Optional[str] = None
    peso: Optional[str] = None
    sexo: Optional[str] = None
    datos_extra: Optional[str] = None

class MascotaResponse(MascotaBase):
    id: int
    cliente_id: int
    datos_extra: Optional[str] = None
    cliente_nombre: Optional[str] = None
    cliente_telefono: Optional[str] = None
    
    class Config:
        from_attributes = True

# --- HISTORIA MEDICA ---
class HistoriaMedicaBase(BaseModel):
    motivo: str
    diagnostico: Optional[str] = None
    tratamiento: Optional[str] = None
    medicamentos: Optional[str] = None
    vacunas: Optional[str] = None
    observaciones: Optional[str] = None

class HistoriaMedicaCreate(HistoriaMedicaBase):
    mascota_id: int

class HistoriaMedicaResponse(HistoriaMedicaBase):
    id: int
    mascota_id: int
    fecha: datetime
    
    class Config:
        from_attributes = True

# --- CLIENTES ---
class ClienteBase(BaseModel):
    nombre: str
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None

class ClienteResponse(ClienteBase):
    id: int
    veterinaria_id: int
    created_at: Optional[datetime] = None
    mascotas: List[MascotaResponse] = []

    class Config:
        from_attributes = True

# --- CITAS ---
class CitaBase(BaseModel):
    fecha_hora: datetime
    motivo: Optional[str] = None
    estado: Optional[str] = "pendiente"

class CitaCreate(CitaBase):
    cliente_id: int
    mascota_id: int

class CitaUpdate(BaseModel):
    fecha_hora: Optional[datetime] = None
    motivo: Optional[str] = None
    estado: Optional[str] = None

class CitaResponse(CitaBase):
    id: int
    cliente_id: int
    mascota_id: int
    veterinaria_id: int
    # Podríamos incluir objetos completos si fuera necesario con Nesting
    
    # Flattened info
    cliente_nombre: Optional[str] = None
    mascota_nombre: Optional[str] = None
    
    class Config:
        from_attributes = True

# --- VIDEOS / FLATTENED VIEWS ---

class PatientCreate(BaseModel):
    nombre_mascota: str
    especie: str
    raza: Optional[str] = None
    edad: Optional[str] = None
    nombre_propietario: str
    telefono_propietario: Optional[str] = None
    datos_extra: Optional[str] = None

class PatientResponse(BaseModel):
    id: int # Mascota ID
    nombre_mascota: str
    especie: str
    raza: Optional[str] = None
    edad: Optional[str] = None
    peso: Optional[str] = None
    sexo: Optional[str] = None
    datos_extra: Optional[str] = None
    created_at: Optional[datetime] = None
    
    # Propietario info
    cliente_id: int
    nombre_propietario: str
    telefono_propietario: Optional[str] = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

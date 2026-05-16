from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr
from datetime import date, datetime
from typing import Optional, List

app = FastAPI(
    title="API PROYECTO E.V CHARGE ",
    description="Sistema  de cargadores electricos en Bogota",
    version="1.0"
)

# 1 MODELO DE CARROS
class carros(BaseModel):
    id: int = Field(gt=0, description="ID del carro, debe ser mayor a 0")
    placa: str = Field(min_length=5, max_length=10, description="Placa del carro (ej: ABC-123)")
    modelo: str = Field(min_length=1, max_length=50, description="Modelo del carro (ej: Toyota Corolla 2024)")
    tipo_cargador: str = Field(min_length=1, description="Tipo de cargador (eléctrico, híbrido, gasolina, diésel)")
    estado: str = Field(min_length=1, description="Estado del carro (cargando, descargando, disponible, mantenimiento)")
    capacidad: float = Field(gt=0, description="Capacidad de carga en kilogramos, debe ser mayor a 0")
    
    


# --- BASES DE DATOS SIMULADAS ---
db_cargadores = [
    {"id": 1, "marca": "Tesla", "tipo": "TIPO B", "estado": "Activo", "cantidad": 5},
    {"id": 2, "marca": "BYD", "tipo": "TIPO C", "estado": "Inactivo", "cantidad": 0},
    {"id": 3, "marca": "Tesla", "tipo": "TIPO A", "estado": "Activo", "cantidad": 3}
]

db_carros = [
    {"placa": "SDF156", "propietario_id": 1001, "estado": "CARGANDO", "marca": "Renault"},
    {"placa": "RGH894", "propietario_id": 1002, "estado": "LIBRE", "marca": "Tesla"}
]

db_usuarios = [
    {"id": 12535633, "nombre": "jhonsito", "estado": "Activo", "tipo": "Premium"},
    {"id": 1565262, "nombre": "juanito", "estado": "Inactivo", "tipo": "Estandar"}
]

# --- 1. ENTIDAD: CARGADORES ---
# Path Params: id | Query Params: marca, estado
@app.get("/cargadores/{id}")
def obtener_cargador(
    id: int = Path(..., gt=0), 
    marca: Optional[str] = Query(None, min_length=3),
    estado: Optional[str] = Query(None)
):
    for c in db_cargadores:
        if c["id"] == id:
            return c
    raise HTTPException(status_code=404, detail="Cargador no encontrado")

# --- 2. ENTIDAD: CARROS ---
# Path Params: placa | Query Params: estado, marca
@app.post("/carros", status_code=201)
def crear_carro(carro: Carro):
    """
    Registra un nuevo carro en el sistema.
    """
    global contador_id
    
    # Verificar que la placa no exista ya
    for c in carros_db:
        if c["placa"] == carro.placa:
            raise HTTPException(status_code=400, detail="Ya existe un carro con esta placa")
    
    # Crear el nuevo carro con ID automático
    nuevo_carro = carro.dict()
    nuevo_carro["id"] = contador_id
    contador_id += 1
    
    carros_db.append(nuevo_carro)
    
    return {
        "mensaje": "Carro registrado exitosamente",
        "carro": nuevo_carro,
        "status": "success"
    }

# --- 3. ENTIDAD: USUARIOS ---
# Path Params: id | Query Params: nombre, tipo
@app.get("/usuarios/{id}")
def obtener_usuario(
    id: int = Path(..., gt=0),
    nombre: Optional[str] = Query(None, min_length=3),
    tipo: Optional[str] = Query(None)
):
    for u in db_usuarios:
        if u["id"] == id:
            return u
    raise HTTPException(status_code=404, detail="Usuario no existe")

# --- RUTA INICIAL ---
@app.get("/")
def home():
    return {"empresa": "EV CHARGE", "estado": "Servidor Activo"}

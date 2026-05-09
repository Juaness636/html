from fastapi import FastAPI, HTTPException, Path, Query
from typing import Optional

app = FastAPI()

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
@app.get("/carros/{placa}")
def obtener_carro(
    placa: str = Path(..., min_length=6, max_length=6),
    estado: Optional[str] = Query(None),
    marca: Optional[str] = Query(None, min_length=3)
):
    for car in db_carros:
        if car["placa"].upper() == placa.upper():
            return car
    raise HTTPException(status_code=404, detail="Vehículo no registrado")

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

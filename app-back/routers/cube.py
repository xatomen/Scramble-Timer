from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, Cube
from typing import List

router = APIRouter()

# Operaciones CRUD para la tabla Cube

# Definimos un modelo para la creación de instancias de Cube
class CubeBase(BaseModel):
    brand: str
    model: str
    fk_cube_type: int
    magnetic: bool

# Definimos un endpoint POST en la ruta "/cube/"
@router.post("/cube/", tags=["Cube"])
def post_cube(cube: CubeBase, db: Session = Depends(get_db)):
    db_cube = Cube(**cube.dict())
    db.add(db_cube)
    db.commit()
    db.refresh(db_cube)
    return db_cube

# Definimos un endpoint GET en la ruta "/cube/{id}"
@router.get("/cube/{id}", tags=["Cube"])
def get_cube(id: int, db: Session = Depends(get_db)):
    db_cube = db.query(Cube).filter(Cube.id_cube == id).first()
    return db_cube

# Definimos un endpoint GET en la ruta "/cube/"
@router.get("/cube/", response_model=List[CubeBase], tags=["Cube"])
def get_cubes(db: Session = Depends(get_db)):
    db_cubes = db.query(Cube).all()
    return db_cubes

# Definimos un endpoint PUT en la ruta "/cube/{id}"
@router.put("/cube/{id}", tags=["Cube"])
def put_cube(id: int, cube: CubeBase, db: Session = Depends(get_db)):
    db_cube = db.query(Cube).filter(Cube.id_cube == id).first()
    db_cube.brand = cube.brand
    db_cube.model = cube.model
    db_cube.fk_cube_type = cube.fk_cube_type
    db_cube.magnetic = cube.magnetic
    db.commit()
    db.refresh(db_cube)
    return db_cube

# Definimos un endpoint DELETE en la ruta "/cube/{id}"
@router.delete("/cube/{id}", tags=["Cube"])
def delete_cube(id: int, db: Session = Depends(get_db)):
    # Obtenemos la instancia de Cube con el id proporcionado
    db_cube = db.query(Cube).filter(Cube.id_cube == id).first()
    # Eliminamos la instancia de Cube de la sesión de la base de datos
    db.delete(db_cube)
    # Confirmamos la transacción para guardar los cambios en la base de datos
    db.commit()
    # Devolvemos la instancia de Cube eliminada
    return db_cube

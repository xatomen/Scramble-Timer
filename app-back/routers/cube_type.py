from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, CubeType

router = APIRouter()

# Operaciones CRUD para la tabla CubeType

# Definimos un modelo para la creación de instancias de CubeType
class CubeTypeBase(BaseModel):
    cube_type: str

# Definimos un endpoint POST en la ruta "/cube_type/"
@router.post("/cube_type/", tags=["CubeType"])
def post_cube_type(cube_type: CubeTypeBase, db: Session = Depends(get_db)):
    # Añadimos la nueva instancia de CubeType a la sesión de la base de datos
    db.add(cube_type)
    # Confirmamos la transacción para guardar los cambios en la base de datos
    db.commit()
    # Refrescamos la instancia de CubeType para obtener los datos actualizados desde la base de datos
    db.refresh(cube_type)
    # Devolvemos la instancia de CubeType creada
    return cube_type

# Definimos un endpoint GET en la ruta "/cube_type/{id}"
@router.get("/cube_type/{id}", tags=["CubeType"])
def get_cube_type(id: int, db: Session = Depends(get_db)):
    # Obtenemos la instancia de CubeType con el id proporcionado
    db_cube_type = db.query(CubeType).filter(CubeType.id_cube_type == id).first()
    # Devolvemos la instancia de CubeType
    return db_cube_type

# Definimos un endpoint GET en la ruta "/cube_type/"
@router.get("/cube_type/", tags=["CubeType"])
def get_cube_types(db: Session = Depends(get_db)):
    # Obtenemos todas las instancias de CubeType
    db_cube_types = db.query(CubeType).all()
    # Devolvemos la lista de instancias de CubeType
    return db_cube_types

# Definimos un endpoint DELETE en la ruta "/cube_type/{id}"
@router.delete("/cube_type/{id}", tags=["CubeType"])
def delete_cube_type(id: int, db: Session = Depends(get_db)):
    # Obtenemos la instancia de CubeType con el id proporcionado
    db_cube_type = db.query(CubeType).filter(CubeType.id_cube_type == id).first()
    # Eliminamos la instancia de CubeType de la sesión de la base de datos
    db.delete(db_cube_type)
    # Confirmamos la transacción para guardar los cambios en la base de datos
    db.commit()
    # Devolvemos la instancia de CubeType eliminada
    return db_cube_type

# Definimos un endpoint PUT en la ruta "/cube_type/{id}"
@router.put("/cube_type/{id}", tags=["CubeType"])
def put_cube_type(id: int, cube_type: CubeTypeBase, db: Session = Depends(get_db)):
    # Obtenemos la instancia de CubeType con el id proporcionado
    db_cube_type = db.query(CubeType).filter(CubeType.id_cube_type == id).first()
    # Actualizamos los campos de la instancia de CubeType con los valores proporcionados
    db_cube_type.cube_type = cube_type.cube_type
    # Confirmamos la transacción para guardar los cambios en la base de datos
    db.commit()
    # Refrescamos la instancia de CubeType para obtener los datos actualizados desde la base de datos
    db.refresh(db_cube_type)
    # Devolvemos la instancia de CubeType actualizada
    return db_cube_type

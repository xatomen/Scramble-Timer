from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, SolveType

router = APIRouter()

# Operaciones CRUD para la tabla SolveType

# Definimos un modelo para la creación de instancias de SolveType
class SolveTypeBase(BaseModel):
    solve_type: str

# Definimos un endpoint POST en la ruta "/solve_type/"
@router.post("/solve_type/", tags=["SolveType"])
def post_solve_type(solve_type: SolveTypeBase, db: Session = Depends(get_db)):
    # Añadimos la nueva instancia de SolveType a la sesión de la base de datos
    db.add(solve_type)
    # Confirmamos la transacción para guardar los cambios en la base de datos
    db.commit()
    # Refrescamos la instancia de SolveType para obtener los datos actualizados desde la base de datos
    db.refresh(solve_type)
    # Devolvemos la instancia de SolveType creada
    return solve_type

# Definimos un endpoint GET en la ruta "/solve_type/{id}"
@router.get("/solve_type/{id}", tags=["SolveType"])
def get_solve_type(id: int, db: Session = Depends(get_db)):
    # Obtenemos la instancia de SolveType con el id proporcionado
    db_solve_type = db.query(SolveType).filter(SolveType.id_solve_type == id).first()
    # Devolvemos la instancia de SolveType
    return db_solve_type

# Definimos un endpoint GET en la ruta "/solve_type/"
@router.get("/solve_type/", tags=["SolveType"])
def get_solve_types(db: Session = Depends(get_db)):
    # Obtenemos todas las instancias de SolveType
    db_solve_types = db.query(SolveType).all()
    # Devolvemos la lista de instancias de SolveType
    return db_solve_types

# Definimos un endpoint DELETE en la ruta "/solve_type/{id}"
@router.delete("/solve_type/{id}", tags=["SolveType"])
def delete_solve_type(id: int, db: Session = Depends(get_db)):
    # Obtenemos la instancia de SolveType con el id proporcionado
    db_solve_type = db.query(SolveType).filter(SolveType.id_solve_type == id).first()
    # Eliminamos la instancia de SolveType de la sesión de la base de datos
    db.delete(db_solve_type)
    # Confirmamos la transacción para guardar los cambios en la base de datos
    db.commit()
    # Devolvemos la instancia de SolveType eliminada
    return db_solve_type

# Definimos un endpoint PUT en la ruta "/solve_type/{id}"
@router.put("/solve_type/{id}", tags=["SolveType"])
def put_solve_type(id: int, solve_type: SolveTypeBase, db: Session = Depends(get_db)):
    # Obtenemos la instancia de SolveType con el id proporcionado
    db_solve_type = db.query(SolveType).filter(SolveType.id_solve_type == id).first()
    # Actualizamos los campos de la instancia de SolveType con los valores proporcionados
    db_solve_type.solve_type = solve_type.solve_type
    # Confirmamos la transacción para guardar los cambios en la base de datos
    db.commit()
    # Refrescamos la instancia de SolveType para obtener los datos actualizados desde la base de datos
    db.refresh(db_solve_type)
    # Devolvemos la instancia de SolveType actualizada
    return db_solve_type

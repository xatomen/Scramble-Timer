from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, Solve

router = APIRouter()

from datetime import datetime, time

## Operaciones CRUD para la tabla Solve

# Definimos un modelo para la creación de instancias de Solve
class SolveBase(BaseModel):
    date: datetime
    time: time
    scramble: str
    fk_cube: int
    fk_solve_type: int
    fk_solve_session: int

# Definimos un endpoint POST en la ruta "/solve/"
@router.post("/solve/", tags=["Solve"])
def post_solve(solve: SolveBase, db: Session = Depends(get_db)):
    # Convertimos el objeto SolveCreate en un diccionario y lo desempaquetamos para crear una instancia de Solve
    db_solve = Solve(**solve.dict())
    # Añadimos la nueva instancia de Solve a la sesión de la base de datos
    db.add(db_solve)
    # Confirmamos la transacción para guardar los cambios en la base de datos
    db.commit()
    # Refrescamos la instancia de Solve para obtener los datos actualizados desde la base de datos
    db.refresh(db_solve)
    # Devolvemos la instancia de Solve creada
    return db_solve

# Definimos un endpoint GET en la ruta "/solve/{id}"
@router.get("/solve/{id}", tags=["Solve"])
def get_solve(id: int, db: Session = Depends(get_db)):
    # Obtenemos la instancia de Solve con el id proporcionado
    db_solve = db.query(Solve).filter(Solve.id_solve == id).first()
    # Devolvemos la instancia de Solve
    return db_solve

# Definimos un endpoint GET en la ruta "/solve/"
@router.get("/solve/", tags=["Solve"])
def get_solves(db: Session = Depends(get_db)):
    # Obtenemos todas las instancias de Solve
    db_solves = db.query(Solve).all()
    # Devolvemos la lista de instancias de Solve
    return db_solves

# Definimos un endpoint DELETE en la ruta "/solve/{id}"
@router.delete("/solve/{id}", tags=["Solve"])
def delete_solve(id: int, db: Session = Depends(get_db)):
    # Obtenemos la instancia de Solve con el id proporcionado
    db_solve = db.query(Solve).filter(Solve.id_solve == id).first()
    # Eliminamos la instancia de Solve de la sesión de la base de datos
    db.delete(db_solve)
    # Confirmamos la transacción para guardar los cambios en la base de datos
    db.commit()
    # Devolvemos la instancia de Solve eliminada
    return db_solve

# Definimos un endpoint PUT en la ruta "/solve/{id}"
@router.put("/solve/{id}", tags=["Solve"])
def put_solve(id: int, solve: SolveBase, db: Session = Depends(get_db)):
    # Obtenemos la instancia de Solve con el id proporcionado
    db_solve = db.query(Solve).filter(Solve.id_solve == id).first()
    # Actualizamos los campos de la instancia de Solve con los valores proporcionados
    db_solve.date = solve.date
    db_solve.time = solve.time
    db_solve.scramble = solve.scramble
    db_solve.fk_cube = solve.fk_cube
    db_solve.fk_solve_type = solve.fk_solve_type
    db_solve.fk_session = solve.fk_session
    # Confirmamos la transacción para guardar los cambios en la base de datos
    db.commit()
    # Refrescamos la instancia de Solve para obtener los datos actualizados desde la base de datos
    db.refresh(db_solve)
    # Devolvemos la instancia de Solve actualizada
    return db_solve

# Session Solve

# Definimos un endpoint POST en la ruta "/session/{id}/solve/"
@router.post("/session/{id}/solve/", tags=["Solve"])
def post_session_solve(id: int, solve: SolveBase, db: Session = Depends(get_db)):
    # Convertimos el objeto SolveCreate en un diccionario y lo desempaquetamos para crear una instancia de Solve
    db_solve = Solve(**solve.dict())
    db_solve.fk_session = id
    # Añadimos la nueva instancia de Solve a la sesión de la base de datos
    db.add(db_solve)
    # Confirmamos la transacción para guardar los cambios en la base de datos
    db.commit()
    # Refrescamos la instancia de Solve para obtener los datos actualizados desde la base de datos
    db.refresh(db_solve)
    # Devolvemos la instancia de Solve creada
    return db_solve

# Definimos un endpoint GET en la ruta "/session/{id}/solve/"
@router.get("/session/{id}/solve/", tags=["Solve"])
def get_session_solves(id: int, db: Session = Depends(get_db)):
    # Obtenemos todas las instancias de Solve de la sesión correspondiente
    db_solves = db.query(Solve).filter(Solve.fk_session == id).all()
    # Devolvemos la lista de instancias de Solve
    return db_solves

# Definimos un endpoint DELETE en la ruta "/session/{id}/solve/{id_solve}"
@router.delete("/session/{id}/solve/{id_solve}", tags=["Solve"])
def delete_session_solve(id: int, id_solve: int, db: Session = Depends(get_db)):
    # Obtenemos la instancia de Solve con el id proporcionado
    db_solve = db.query(Solve).filter(Solve.id_solve == id_solve).first()
    # Eliminamos la instancia de Solve de la sesión de la base de datos
    db.delete(db_solve)
    # Confirmamos la transacción para guardar los cambios en la base de datos
    db.commit()
    # Devolvemos la instancia de Solve eliminada
    return db_solve

# Definimos un endpoint PUT en la ruta "/session/{id}/solve/{id_solve}"
@router.put("/session/{id}/solve/{id_solve}", tags=["Solve"])
def put_session_solve(id: int, id_solve: int, solve: SolveBase, db: Session = Depends(get_db)):
    # Obtenemos la instancia de Solve con el id proporcionado
    db_solve = db.query(Solve).filter(Solve.id_solve == id_solve).first()
    # Actualizamos los campos de la instancia de Solve con los valores proporcionados
    db_solve.date = solve.date
    db_solve.time = solve.time
    db_solve.scramble = solve.scramble
    db_solve.fk_cube = solve.fk_cube
    db_solve.fk_solve_type = solve.fk_solve_type
    # Confirmamos la transacción para guardar los cambios en la base de datos
    db.commit()
    # Refrescamos la instancia de Solve para obtener los datos actualizados desde la base de datos
    db.refresh(db_solve)
    # Devolvemos la instancia de Solve actualizada
    return db_solve
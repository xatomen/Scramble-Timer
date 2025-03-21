from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, Session as SessionModel, Solve

router = APIRouter()

# Operaciones CRUD para la tabla Session

# Definimos un modelo para la creación de instancias de Session
class SessionBase(BaseModel):
    name: str
    avg: int
    ao5: int
    ao12: int
    qty: int
    fk_user: int

# Definimos un endpoint POST en la ruta "/session/"
@router.post("/session/", tags=["Session"])
def post_session(session: SessionBase, db: Session = Depends(get_db)):
    # Convertimos el modelo de Pydantic a una instancia de la clase Session de SQLAlchemy
    db_session = SessionModel(**session.dict())
    # Añadimos la nueva instancia de Session a la sesión de la base de datos
    db.add(db_session)
    # Confirmamos la transacción para guardar los cambios en la base de datos
    db.commit()
    # Refrescamos la instancia de Session para obtener los datos actualizados desde la base de datos
    db.refresh(db_session)
    # Devolvemos la instancia de Session creada
    return db_session

# Definimos un endpoint GET en la ruta "/session/{id}"
@router.get("/session/{id}", tags=["Session"])
def get_session(id: int, db: Session = Depends(get_db)):
    # Obtenemos la instancia de Session con el id proporcionado
    db_session = db.query(SessionModel).filter(SessionModel.id_session == id).first()
    # Devolvemos la instancia de Session
    return db_session

# Definimos un endpoint GET en la ruta "/session/"
@router.get("/session/", tags=["Session"])
def get_sessions(user_id: int, db: Session = Depends(get_db)):
    # Obtenemos todas las instancias de Session del usuario correspondiente
    db_sessions = db.query(SessionModel).filter(SessionModel.fk_user == user_id).all()
    # Devolvemos la lista de instancias de Session
    return db_sessions

# Definimos un endpoint DELETE en la ruta "/session/{id}"
@router.delete("/session/{id}", tags=["Session"])
def delete_session(id: int, db: Session = Depends(get_db)):
    # Obtenemos la instancia de Session con el id proporcionado
    db_session = db.query(SessionModel).filter(SessionModel.id_session == id).first()
    # Eliminamos la instancia de Session de la sesión de la base de datos
    db.delete(db_session)
    # Confirmamos la transacción para guardar los cambios en la base de datos
    db.commit()
    # Devolvemos la instancia de Session eliminada
    return db_session

# Definimos un endpoint PUT en la ruta "/session/{id}"
@router.put("/session/{id}", tags=["Session"])
def put_session(id: int, session: SessionBase, db: Session = Depends(get_db)):
    # Obtenemos la instancia de Session con el id proporcionado
    db_session = db.query(SessionModel).filter(SessionModel.id_session == id).first()
    
    # Obtenemos todas las solves de la sesión
    solves = db.query(Solve).filter(Solve.fk_session == id).all()
    
    # Calculamos los tiempos en segundos
    times = [solve.time.hour * 3600 + solve.time.minute * 60 + solve.time.second + solve.time.microsecond / 1e6 for solve in solves]
    
    # Calculamos avg, ao5 y ao12
    if times:
        db_session.avg = sum(times) / len(times)
        db_session.ao5 = sum(sorted(times)[:5]) / 5 if len(times) >= 5 else None
        db_session.ao12 = sum(sorted(times)[:12]) / 12 if len(times) >= 12 else None
    else:
        db_session.avg = None
        db_session.ao5 = None
        db_session.ao12 = None
    
    # Actualizamos la cantidad de solves
    db_session.qty = len(solves)
    
    # Actualizamos el nombre de la sesión
    db_session.name = session.name
    
    # Confirmamos la transacción para guardar los cambios en la base de datos
    db.commit()
    # Refrescamos la instancia de Session para obtener los datos actualizados desde la base de datos
    db.refresh(db_session)
    # Devolvemos la instancia de Session actualizada
    return db_session
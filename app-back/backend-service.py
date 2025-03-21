# Servicio backend para la aplicación utilizando FastAPI

# Importamos fastapi
from fastapi import FastAPI

# Importamos los routers
from routers import session
from routers import solve_type
from routers import cube_type
from routers import cube
from routers import solve
from routers import user

# Inicialización de la aplicación
app = FastAPI()

app.include_router(session.router)
app.include_router(solve_type.router)
app.include_router(cube_type.router)
app.include_router(cube.router)
app.include_router(solve.router)
app.include_router(user.router)


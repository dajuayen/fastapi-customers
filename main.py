from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette_prometheus import metrics, PrometheusMiddleware

from config.database import engine, Base, get_db
from controllers.user import UserController
from routers import customers, users, securities

Base.metadata.create_all(bind=engine)
app = FastAPI()

# Prueba de añadir un middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics/", metrics)

# Grupos de endpoints añadidos
app.include_router(securities.router)
app.include_router(customers.router)
app.include_router(users.router)


@app.get("/")
def main(db: Session = Depends(get_db)):
    UserController(db).create_admin_user()
    return RedirectResponse(url="/docs/")

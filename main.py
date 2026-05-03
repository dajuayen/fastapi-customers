from elasticapm import get_client
from elasticapm.contrib.starlette import make_apm_client, ElasticAPM
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette_prometheus import metrics, PrometheusMiddleware

from config.database import engine, Base, get_db
from config.logger import logger
from config.settings import settings
from controllers.user import UserController
from routers import customers, users, securities

app = FastAPI()

apm_client = None
if settings.ELASTIC_APM_ENABLED:
    apm_client = get_client()
    if apm_client is None:
        apm_client = make_apm_client(
            {
                "SERVICE_NAME": settings.ELASTIC_APM_SERVICE_NAME,
                "SERVER_URL": settings.ELASTIC_APM_SERVER_URL,
                "ENVIRONMENT": settings.ELASTIC_APM_ENVIRONMENT,
            }
        )
    # Instrumentar sqlite/psycopg2 antes de crear conexiones; add_middleware hace instrument().
    app.add_middleware(ElasticAPM, client=apm_client)


Base.metadata.create_all(bind=engine)


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
def main(session: Session = Depends(get_db)):
    """Root endpoint of the app
    Args:
        session: Session
    Returns: response
    """
    logger.info("GET / ")
    # apm.capture_message('GET /  hello, world!')
    UserController(session).create_admin_user()
    logger.info("GET / completado")
    return RedirectResponse(url="/docs/")


@app.get("/test")
def test_endpoint(session: Session = Depends(get_db)):
    """Endpoint de prueba para verificar trazas en APM"""
    logger.info("GET /test - iniciando")

    # Esto genera una transacción automática gracias al middleware ElasticAPM
    UserController(session).create_admin_user()

    logger.info("GET /test - completado")
    return {"status": "ok", "message": "Transacción registrada en APM"}

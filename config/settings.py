import os
from pathlib import Path

from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Class to collect environment variables"""

    env: str = os.getenv("env", "test")

    db_name: str = os.getenv("DB_NAME")
    db_user: str = os.getenv("DB_USER")
    db_pass: str = os.getenv("DB_PASS")
    db_host: str = os.getenv("DB_HOST")
    db_port: str = os.getenv("DB_PORT")

    ELASTIC_APM_ENABLED: bool = (
        os.getenv("ELASTIC_APM_ENABLED", "true").lower() == "true"
    )
    ELASTIC_APM_SERVER_URL = os.getenv("ELASTIC_APM_SERVER_URL")
    ELASTIC_APM_SERVICE_NAME = os.getenv("ELASTIC_APM_SERVICE_NAME")
    ELASTIC_APM_ENVIRONMENT = os.getenv("ELASTIC_APM_ENVIRONMENT")

    SQLALCHEMY_POSTGRES_URL = os.getenv("POSTGRES_URL")

    @property
    def path_base(self):
        """Get project's main folder url.
        Returns: str
        """
        path_aux = Path(os.getcwd())
        contenido = os.listdir(path_aux.as_posix())
        founded = "main.py" in contenido and "config" in contenido
        intents = 3
        while not founded and intents > 0:
            path_aux = Path(path_aux.parent.absolute())
            contenido = os.listdir(path_aux.as_posix())
            founded = "main.py" in contenido and "config" in contenido
            intents -= 1
        return path_aux.as_posix()

    @property
    def SQLALCHEMY_SQLITE_URL(self):  # pylint: disable=C0103
        """Get SQLAlchemy connection url.
        Returns: str
        """
        return f"sqlite:///{self.path_base}/{os.getenv('SQLITE_FILE_URL')}"


settings = Settings()

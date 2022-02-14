import os
from pathlib import Path

from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Class to collect environment variables"""

    env: str = os.getenv('env', "test")

    db_name: str = os.getenv('DB_NAME')
    db_user: str = os.getenv('DB_USER')
    db_pass: str = os.getenv('DB_PASS')
    db_host: str = os.getenv('DB_HOST')
    db_port: str = os.getenv('DB_PORT')

    @property
    def path_base(self):
        """Get project's main folder url.
        Returns: str
        """
        path_aux = Path(os.getcwd())
        contenido = os.listdir(path_aux.as_posix())
        founded = ".env" in contenido and "config" in contenido
        while not founded:
            path_aux = Path(path_aux.parent.absolute())
            contenido = os.listdir(path_aux.as_posix())
            founded = ".env" in contenido and "config" in contenido
        return path_aux.as_posix()


settings = Settings()

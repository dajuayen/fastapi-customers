import logging.config
import os

from pydantic import BaseModel

from config.settings import settings


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = settings.ELASTIC_APM_SERVICE_NAME or "customers"
    LOG_FORMAT: str = (
        "%(levelprefix)s | %(asctime)s | [%(name)s.%(funcName)s] | %(message)s"
    )
    LOG_LEVEL: str = "INFO"

    version: int = 1
    disable_existing_loggers: bool = False

    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%d-%m-%Y %H:%M:%S",
        },
        "ecs": {
            "()": "ecs_logging.StdlibFormatter",
        },
    }

    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "elasticapm": {
            "level": "INFO",
            "class": "elasticapm.handlers.logging.LoggingHandler",
            "formatter": "ecs",
        },
    }

    def get_config(self):
        """Get logging configuration"""
        # Determinar qué handlers usar según si APM está habilitado
        apm_enabled = os.getenv("ELASTIC_APM_ENABLED", "true").lower() == "true"
        handlers_list = ["default"]
        if apm_enabled:
            handlers_list.append("elasticapm")

        return {
            "version": self.version,
            "disable_existing_loggers": self.disable_existing_loggers,
            "formatters": self.formatters,
            "handlers": self.handlers,
            "loggers": {
                self.LOGGER_NAME: {
                    "handlers": handlers_list,  # ← Solo agrega elasticapm si está habilitado
                    "level": self.LOG_LEVEL,
                    "propagate": False,
                },
            },
        }


loging_config = LogConfig()
logging.config.dictConfig(loging_config.get_config())
logger = logging.getLogger(loging_config.LOGGER_NAME)

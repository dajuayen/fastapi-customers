import logging

from pydantic import BaseModel

from config.settings import settings


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    # Debe coincidir con el nombre del logger global (handlers ECS + ElasticAPM).
    LOGGER_NAME: str = settings.ELASTIC_APM_SERVICE_NAME or "customers"

    LOG_FORMAT: str = (
        "%(levelprefix)s | %(asctime)s | [%(name)s.%(funcName)s] | %(message)s"
    )
    LOG_LEVEL: str = "INFO"

    # Logging config (consola + envío ECS al agente APM vía LoggingHandler).
    version: int = 1
    disable_existing_loggers: bool = False

    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%d-%m-%Y %H:%M:%S",
        },
        "ecs": {
            "()": "ecs_logging.StdlibFormatter",  # Formato JSON que entiende Elastic [3]
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
            "formatter": "ecs",  # Aplica el formato ECS aquí
        },
    }

    def get_config(self):
        """Get logging configuration"""
        return {
            "version": self.version,
            "disable_existing_loggers": self.disable_existing_loggers,
            "formatters": self.formatters,
            "handlers": self.handlers,
            "loggers": {
                self.LOGGER_NAME: {
                    "handlers": ["default", "elasticapm"],
                    "level": self.LOG_LEVEL,
                    "propagate": False,
                },
            },
        }


logging_config = LogConfig()
logging.config.dictConfig(logging_config.get_config())
logger = logging.getLogger(logging_config.LOGGER_NAME)

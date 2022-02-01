# Add ann ECS formatter to the Handler
import logging

import fastapi.logger as fast_logger

import ecs_logging
from elasticapm.contrib.starlette import make_apm_client

HANDLER = logging.StreamHandler()
HANDLER.setFormatter(ecs_logging.StdlibFormatter())
#
# apm = make_apm_client({
#     'SERVICE_NAME': 'CUSTOMERS',
#     'DEBUG': True,
#     'SERVER_URL': 'http://localhost:8200',
#     'CAPTURE_HEADERS': True,
#     'CAPTURE_BODY': 'all'
# })

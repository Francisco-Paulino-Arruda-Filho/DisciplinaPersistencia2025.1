

from logging.config import setup_logging


def log_request(request):
    """
    Log the incoming request details.
    """
    logger = setup_logging.getLogger(__name__)
    logger.info(f"Request: {request.method} {request.url}")
    if request.method in ["POST", "PUT", "PATCH"]:
        logger.info(f"Request Body: {request.json()}")
    if request.method in ["GET", "DELETE"]:
        logger.info(f"Request Params: {request.query_params}")
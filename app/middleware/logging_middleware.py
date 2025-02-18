import time
import logging
from fastapi import Request

logger = logging.getLogger("BIRTHDAY_ANIME")

async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(
        f"Incoming request:\n"
        f"  - Method: {request.method}\n"
        f"  - URL: {request.url}\n"
        f"  - User-Agent: {request.headers.get('user-agent')}\n"
        f"  - Content-Type: {request.headers.get('content-type')}\n"
        f"  - Accept: {request.headers.get('accept')}"
    )
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        logger.info(
            f"Response sent:\n"
            f"  - Status: {response.status_code}\n"
            f"  - Processing time: {duration:.2f} seconds\n"
            f"  - Content-Type: {response.headers.get('content-type')}\n"
            f"  - Content-Length: {response.headers.get('content-length')}"
        )
        return response
    except Exception as e:
        logger.error(
            f"Processing error:\n"
            f"  - Error type: {type(e).__name__}\n"
            f"  - Description: {str(e)}\n"
            f"  - Time until error: {time.time() - start_time:.2f} seconds"
        )
        raise

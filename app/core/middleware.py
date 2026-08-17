import logging
import time
from collections.abc import Awaitable, Callable

from fastapi import Request, Response

from app.core.request_id import set_request_id

logger = logging.getLogger("api")


async def request_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    request_id = set_request_id(request.headers.get("X-Request-ID"))
    start = time.perf_counter()

    response = await call_next(request)

    elapsed_ms = (time.perf_counter() - start) * 1000

    logger.info(
        f"{request.method} {request.url.path} {response.status_code} {elapsed_ms:.1f}ms",
        extra={"request_id": request_id},
    )

    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{elapsed_ms:.1f}"
    return response

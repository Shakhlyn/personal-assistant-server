import contextvars
import uuid

request_id_ctx: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "request_id",
    default=None,
)


def get_request_id() -> str | None:
    return request_id_ctx.get()


def set_request_id(incoming: str | None = None) -> str:
    """Reuse the caller's X-Request-ID when present so traces stitch across services."""
    rid = incoming or str(uuid.uuid4())
    request_id_ctx.set(rid)
    return rid

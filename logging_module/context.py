import uuid
from contextvars import ContextVar

correlation_id: ContextVar[uuid.UUID] = ContextVar(
    'correlation_id', default=uuid.UUID('00000000-0000-0000-0000-000000000000')
)

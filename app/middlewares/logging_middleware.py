import uuid
import logging
from fastapi import Request

from starlette.middleware.base import BaseHTTPMiddleware


logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        
    async def set_body(self, request: Request):
        receive_ = await request._receive()
        async def receive():
            return receive_
        request._receive = receive
    
    async def dispatch(self, request, call_next):
        await self.set_body(request)
        request.state.request_id = request.headers.get("x-request-id")
        request_id = request.state.request_id
        body = {}
        try:
            body = await request.json()
        except:
            body = {}
        logger.info(
            "Incomming request",
            extra={
                "request_id": request_id if request_id else None,
                "method": str(request.method).upper(),
                "path": str(request.url.path),
                "params": str(request.query_params),
                'body': body,
                "user_id": request.state.userdata.id if hasattr(request.state, 'userdata') else None
            },
        )

        response = await call_next(request)
        return response
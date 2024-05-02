import logging
import uvicorn

from fastapi import Depends, FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers.v1 import v1_router
from app.core.exceptions import APIException
from app.middlewares.logging_middleware import LoggingMiddleware


logger = logging.getLogger(__name__)

app = FastAPI(
    title="Foodcheck",
    description="",
    version="0.0.1",
    contact={
        "name": "Thanh Tran Nhat",
        "email": "nhatthanh020996@gmail.com",
    },
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)


app.include_router(v1_router)


@app.on_event("startup")
async def startup_event():
    logger.info("Webserver's ready to listen incomming requests!")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Terminated webserver successfully!!!")


@app.exception_handler(APIException)
async def http_exception_handler(request: Request, exc: APIException):
    request_id = request.state.request_id
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': '*',
        'Access-Control-Allow-Headers': '*'
    }
    return JSONResponse(
        status_code=exc.status, 
        content={
            "message": exc.message, "error_code": exc.error_code, 'trace_id': request_id
        }, 
        headers=headers
    )


@app.exception_handler(Exception)
async def http_exception_handler(request: Request, exc: Exception):
    request_id = request.state.request_id
    body = {}
    try:
        body = await request.json()
    except:
        body = {}
    logger.exception(
        'Unexpected Exception Occurs',
        extra={
            'request_id': request_id,
            "method": str(request.method).upper(),
            "path": str(request.url.path),
            "params": str(request.query_params),
            'body': body,
            "user_id": request.state.userdata.id if hasattr(request.state, 'userdata') else None
        }
    )
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': '*',
        'Access-Control-Allow-Headers': '*'
    }
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        content={
            "message": 'A server error occurred.', 'trace_id': request_id
        },
        headers=headers
    )

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level="debug", proxy_headers=True)

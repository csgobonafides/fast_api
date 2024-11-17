from pathlib import Path
from fastapi import FastAPI, Request
from src.api.items import router as items_router
import logging
from contextlib import asynccontextmanager
from src.core.logger_config import init_logger, LOGGING_CONFIG
from starlette.responses import JSONResponse
from src.storages.jsonfilestorage import JsonFileStorage
from time import monotonic
import src.controllers.work_to_db as c


@asynccontextmanager
async def lifespan(_app: FastAPI):
    dir = Path(__file__).parent.parent
    lamp_db = JsonFileStorage(dir /'db.json')
    await lamp_db.connect()
    c.controller = c.Controller(lamp_db)
    yield
    await lamp_db.disconnect()


init_logger()
logger = logging.getLogger(__name__)
app = FastAPI(lifespan=lifespan, title='FastAPI')
app.include_router(items_router, tags=['comands'], prefix='/items')



@app.exception_handler(Exception)
async def common_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            'message': (
                f'Failed method {request.method} at URL {request.url}'
                f'exception message is {exc!r}.'
            )
        },
    )


@app.middleware('http')
async def time_log_middleware(request: Request, call_next):
    start_time = monotonic()
    try:
        return await call_next(request)
    finally:
        finish_time = 1000.0 * (monotonic() - start_time)
        process_time = '{:0.6f}|ms'.format(finish_time)
        logger.info(f'Response: {request.url.path} Duration {process_time}')



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000, log_config=LOGGING_CONFIG)
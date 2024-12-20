from fastapi import FastAPI, Request
from databases import Database
from api.lamps import router as lamp_router
from api.manufacturers import router as manufacturer_router
import logging
from contextlib import asynccontextmanager
from starlette.responses import JSONResponse
from time import monotonic
from core.settings import get_settings

import controllers.lamp as lamp_modul
import controllers.manufacturer as manufacturer_modul

config = get_settings()
db = Database(config.dsn())
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("Do something at application startup")
    await db.connect()
    manufacturer_modul.manufacturer_controller = manufacturer_modul.ManufacturerController(db)
    lamp_modul.lamp_controller = lamp_modul.LampController(db)
    yield
    logger.info("Do something at application shutdown")
    await db.disconnect()


app = FastAPI(lifespan=lifespan, title='FastAPI')
app.include_router(manufacturer_router, tags=['manufacturer'], prefix='/manufacturer')
app.include_router(lamp_router, tags=['lamp'], prefix='/lamp')


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
    uvicorn.run(app, host='127.0.0.1', port=8000, log_config="core/logging.yaml")

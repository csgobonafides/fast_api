from fastapi import FastAPI
from src.api.items import router as items_router


app = FastAPI(title='FastAPI')
app.include_router(items_router, tags=['comands'], prefix='/items')


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
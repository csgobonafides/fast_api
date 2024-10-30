from fastapi import FastAPI
from src.api.router_api import router_api


app = FastAPI(title='FastAPI')
app.include_router(router_api, tags=['comands'])


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
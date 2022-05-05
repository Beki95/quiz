import uvicorn
from fastapi import FastAPI

from apps.questions import router
from core.base_db import database

app = FastAPI()

app.include_router(router, prefix='/questions', tags=['questions'])


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


if __name__ == '__main__':
    uvicorn.run(app="main:app", port=8000, host="0.0.0.0", reload=True)

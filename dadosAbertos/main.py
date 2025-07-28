from fastapi import FastAPI
from database import init_db
from routers.bens_e_direitos import router as bens_e_direitos_router

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(bens_e_direitos_router, prefix="/bens_e_direitos", tags=["Bens e Direitos"])
from fastapi import FastAPI
from routes.professor import router as professores_router
from routes.alunos import router as alunos_router
from routes.avancadas import router as avancadas_router

app = FastAPI()
app.include_router(professores_router, prefix="/professores", tags=["Professores"])
app.include_router(alunos_router, prefix="/alunos", tags=["Alunos"])
app.include_router(avancadas_router, prefix="/avancadas", tags=["Avançadas"])
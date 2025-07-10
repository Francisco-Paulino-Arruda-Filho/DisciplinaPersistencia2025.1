from fastapi import FastAPI
from routes.professor import router as professores_router
from routes.alunos import router as alunos_router
from routes.avancadas import router as avancadas_router
from routes.cursos import router as cursos_router
from routes.turmas import router as turmas_router
from routes.matriculas import router as matriculas_router   

app = FastAPI()
app.include_router(professores_router, prefix="/professores", tags=["Professores"])
app.include_router(alunos_router, prefix="/alunos", tags=["Alunos"])
app.include_router(cursos_router, prefix="/cursos", tags=["Cursos"])
app.include_router(turmas_router, prefix="/turmas", tags=["Turmas"])
app.include_router(matriculas_router, prefix="/matriculas", tags=["Matriculas"])
app.include_router(avancadas_router, prefix="/avancadas", tags=["Avançadas"])
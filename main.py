from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configurando o CORS para permitir requisições de qualquer origem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de dados para a requisição
class DataRequest(BaseModel):
    name: str
    age: int

# Endpoint para receber uma requisição POST
@app.post("/submit")
async def receive_data(data: DataRequest):
    # Verificação simples
    if data.age < 0:
        raise HTTPException(status_code=400, detail="A idade não pode ser negativa")
    
    # Responder com uma mensagem de confirmação
    return {"message": f"Dados recebidos: Nome - {data.name}, Idade - {data.age}"}

# Rodar o servidor FastAPI usando:
# uvicorn main:app --reload

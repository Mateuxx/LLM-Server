import asyncio
import httpx

# Função para enviar uma única requisição para o endpoint /submit
async def send_request(client, name, age):
    url = "http://127.0.0.1:8002/submit"
    data = {
        "name": name,
        "age": age
    }
    
    try:
        response = await client.post(url, json=data)
        if response.status_code == 200:
            print(f"Resposta para {name}, {age}: {response.json()}")
        else:
            print(f"Erro {response.status_code} para {name}, {age}")
    except httpx.RequestError as exc:
        print(f"Erro ao fazer requisição para {exc.request.url!r}.")

# Função principal para disparar várias requisições simultâneas
async def send_multiple_requests():
    async with httpx.AsyncClient() as client:
        tasks = []
        
        # Criar várias requisições para diferentes usuários
        for i in range(1, 11):  # Manda 10 requisições (ajuste conforme necessário)
            name = f"User_{i}"
            age = 20 + i  # Apenas para variar um pouco as idades
            tasks.append(send_request(client, name, age))
        
        # Aguarda todas as requisições serem completadas
        await asyncio.gather(*tasks)

# Executa o script de forma assíncrona
if __name__ == "__main__":
    asyncio.run(send_multiple_requests())

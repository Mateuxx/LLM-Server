import httpx
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

# Função para enviar uma requisição para o endpoint /generate
def send_request(prompt, retries=5, backoff_factor=2.0):
    url = "http://10.205.2.35:8000/generate"  # Endpoint da sua API
    data = {
        "prompt": prompt
    }

    for attempt in range(retries):  # Tenta até 'retries' vezes
        start_time = time.time()  # Captura o tempo de início da requisição
        try:
            response = httpx.post(url, json=data, timeout=200.0)
            elapsed_time = time.time() - start_time  # Calcula o tempo de resposta

            if response.status_code == 200:
                # Imprime a resposta recebida do servidor
                response_json = response.json()
                print(f"Tempo de resposta: {elapsed_time:.2f} segundos | Resposta: {response_json}")
                return {'elapsed_time': elapsed_time, 'response': response_json}  # Retorna o tempo e a resposta
            else:
                # Trata erros HTTP não bem-sucedidos
                print(f"Erro HTTP: {response.status_code} - {response.text}")
                # Retentativa para erros 500 (falha no servidor)
                if response.status_code >= 500:
                    continue
                return None
        except httpx.TimeoutException:
            print(f"Timeout ao conectar com o servidor - Tentativa {attempt + 1} de {retries}")
        except httpx.RequestError as e:
            # Trata erros de requisição (ex: problemas de rede)
            print(f"Erro ao conectar com o servidor: {str(e)} - Tentativa {attempt + 1} de {retries}")

        # Espera com backoff exponencial entre tentativas
        if attempt < retries - 1:
            wait_time = backoff_factor ** (attempt + 1)  # Aumenta mais o tempo entre tentativas
            print(f"Aguardando {wait_time:.2f} segundos antes de tentar novamente...")
            time.sleep(wait_time)

    # Se todas as tentativas falharem, retorna None
    return None

# Função para gerar prompts aleatoriamente entre pequenos e médios
def generate_prompt(i):
    prompt_type = random.choice(["pequeno", "medio"])  # Escolhe aleatoriamente o tipo de prompt
    if prompt_type == "pequeno":
        return f"Teste {i}: Por favor, me diga qual é a capital do Brasil?"
    else:
        # Limitar o tamanho do prompt médio para evitar sobrecarga
        return f"Teste {i}: Por favor, explique de forma concisa um tópico relacionado a ciência e tecnologia."

# Função principal para disparar várias requisições usando threads
def send_multiple_requests():
    prompts = [generate_prompt(i) for i in range(1, 26)]  # Gera os prompts de forma aleatória
    responses = []

    # Usa ThreadPoolExecutor para executar as requisições em paralelo
    with ThreadPoolExecutor(max_workers=5) as executor:  # Ajuste o número de threads conforme necessário
        future_to_prompt = {executor.submit(send_request, prompt): prompt for prompt in prompts}

        for future in as_completed(future_to_prompt):
            prompt = future_to_prompt[future]
            try:
                response = future.result()
                responses.append(response)
            except Exception as e:
                print(f"Ocorreu um erro ao processar o prompt '{prompt}': {str(e)}")

    return responses

# Função para calcular o tempo médio de resposta
def calculate_average_response_time(times):
    # Extrai os tempos válidos da lista de respostas
    valid_times = [t['elapsed_time'] for t in times if t is not None]  # Considera apenas os tempos válidos
    if valid_times:
        avg_time = sum(valid_times) / len(valid_times)
        print(f"Média do tempo de resposta: {avg_time:.2f} segundos")
    else:
        print("Nenhuma resposta válida para calcular o tempo médio.")

# Executa o script
if __name__ == "__main__":
    start_time = time.time()

    # Envia múltiplas requisições
    responses = send_multiple_requests()

    # Calcula o tempo total e a média das respostas
    total_time = time.time() - start_time
    print(f"Tempo total: {total_time:.2f} segundos")

    # Verifica a média do tempo de resposta se houver respostas válidas
    if responses:
        calculate_average_response_time(responses)

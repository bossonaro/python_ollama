# Usando requests diretamente
# Requisições simples
import requests

def consulta_ollama_requests(prompt, modelo, host):
    """
    Faz uma consulta ao Ollama usando a biblioteca requests
    """
    url = f"{host}/api/generate"
    payload = {
        "model": modelo,
        "prompt": prompt,
        "stream": False
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()['response']
    else:
        return f"Erro: {response.status_code}"

if __name__ == "__main__":
    HOST = "http://192.168.0.190:11434"
    PROMPT = "Qual é a capital do Brasil?"
    MODELO = "llama3.2"
    
    # Usando requests
    print("Resposta usando requests:")
    resposta1 = consulta_ollama_requests(PROMPT, MODELO, HOST)
    print(resposta1)
    

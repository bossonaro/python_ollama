# Usando HTTPx
# Alternativa moderna ao requests
# Suporte melhor a HTTP/2
# Requer: pip install httpx
import httpx

def consulta_httpx(prompt, modelo, host):
    """
    Consulta usando HTTPx com suporte a async
    """
    url = f"{host}/api/generate"
    payload = {
        "model": modelo,
        "prompt": prompt,
        "stream": False
    }
    
    with httpx.Client() as client:
        response = client.post(url, json=payload)
        if response.status_code == 200:
            return response.json()['response']
        return f"Erro: {response.status_code}"

if __name__ == "__main__":
    HOST = "http://192.168.0.190:11434"
    PROMPT = "Qual é a capital do Brasil?"
    MODELO = "llama3.2"
    
    # Usando HTTPx
    print("\nResposta usando HTTPx:")
    resposta3 = consulta_httpx(PROMPT, MODELO, HOST)
    print(resposta3)
# Usando aiohttp para requisições assíncronas
# Requisições em paralelo 
# Requer: pip install aiohttp
import aiohttp
import asyncio

async def consulta_aiohttp(prompt, modelo, host):
    """
    Consulta assíncrona usando aiohttp
    """
    url = f"{host}/api/generate"
    payload = {
        "model": modelo,
        "prompt": prompt,
        "stream": False
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                return data['response']
            return f"Erro: {response.status}"

# Exemplo de uso
if __name__ == "__main__":
    HOST = "http://192.168.0.190:11434"
    PROMPT = "Qual é a capital do Brasil?"
    MODELO = "llama3.2"

# Usando aiohttp (precisa ser executado em um loop assíncrono)
    print("\nResposta usando aiohttp:")
    resposta4 = asyncio.run(consulta_aiohttp(PROMPT, MODELO, HOST))
    print(resposta4)
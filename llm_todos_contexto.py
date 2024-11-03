import requests
from langchain_ollama import OllamaLLM
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from litellm import completion
import httpx
import asyncio
import aiohttp

# Prompt de sistema padrão que define o comportamento
DEFAULT_SYSTEM_PROMPT = """
Por favor, siga estas diretrizes ao responder:
- Se você não souber a resposta, diga claramente "Não sei" ou "Não tenho certeza"
- Não invente informações
- Seja conciso e direto nas respostas
- Sempre que possível, cite suas fontes
- Se a pergunta for ambígua, peça esclarecimentos
- Mantenha um tom profissional e objetivo
"""

# Opção 1: Usando requests
def consulta_ollama_requests(prompt, modelo, host, sistema_prompt=DEFAULT_SYSTEM_PROMPT):
    """
    Faz uma consulta ao Ollama usando requests com prompt de sistema
    """
    url = f"{host}/api/generate"
    prompt_completo = f"{sistema_prompt}\n\nPergunta: {prompt}\n\nResposta:"
    
    payload = {
        "model": modelo,
        "prompt": prompt_completo,
        "stream": False
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()['response']
    else:
        return f"Erro: {response.status_code}"

# Opção 2: Usando LangChain
def consulta_langchain(prompt, modelo, host, sistema_prompt=DEFAULT_SYSTEM_PROMPT):
    """
    Consulta usando LangChain com prompt de sistema
    """
    llm = OllamaLLM(
        base_url=host,
        model=modelo,
        callbacks=[StreamingStdOutCallbackHandler()]
    )
    prompt_completo = f"{sistema_prompt}\n\nPergunta: {prompt}\n\nResposta:"
    return llm.invoke(prompt_completo)

# Opção 3: Usando LiteLLM
def consulta_litellm(prompt, modelo, host, sistema_prompt=DEFAULT_SYSTEM_PROMPT):
    """
    Consulta usando LiteLLM com suporte a mensagens de sistema
    """
    response = completion(
        model=f"ollama/{modelo}",
        messages=[
            {"role": "system", "content": sistema_prompt},
            {"role": "user", "content": prompt}
        ],
        api_base=host
    )
    return response.choices[0].message.content

# Opção 4: Usando HTTPx
def consulta_httpx(prompt, modelo, host, sistema_prompt=DEFAULT_SYSTEM_PROMPT):
    """
    Consulta usando HTTPx com prompt de sistema
    """
    url = f"{host}/api/generate"
    prompt_completo = f"{sistema_prompt}\n\nPergunta: {prompt}\n\nResposta:"
    
    payload = {
        "model": modelo,
        "prompt": prompt_completo,
        "stream": False
    }
    timeout = httpx.Timeout(10.0, connect=5.0)  # 10s para a resposta, 5s para conexão
    with httpx.Client(timeout=timeout) as client:
        response = client.post(url, json=payload)
        if response.status_code == 200:
            return response.json()['response']
        return f"Erro: {response.status_code}"

# Opção 5: Usando aiohttp (assíncrono)
async def consulta_aiohttp(prompt, modelo, host, sistema_prompt=DEFAULT_SYSTEM_PROMPT):
    """
    Consulta assíncrona usando aiohttp com prompt de sistema
    """
    url = f"{host}/api/generate"
    prompt_completo = f"{sistema_prompt}\n\nPergunta: {prompt}\n\nResposta:"
    
    payload = {
        "model": modelo,
        "prompt": prompt_completo,
        "stream": False
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                return data['response']
            return f"Erro: {response.status}"

# Função auxiliar para carregar prompts de sistema de um arquivo
def carregar_prompt_sistema(arquivo):
    """
    Carrega um prompt de sistema de um arquivo de texto
    """
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return DEFAULT_SYSTEM_PROMPT

# Exemplo de uso
if __name__ == "__main__":
    HOST = "http://192.168.0.190:11434"
    MODELO = "llama3.2"
    
    # Você pode personalizar o prompt de sistema aqui
    MEU_PROMPT_SISTEMA = """
    Você é um assistente especializado em tecnologia da informação.
    Suas respostas devem ser:
    - Técnicas e precisas
    - Baseadas em fatos verificáveis
    - Com exemplos práticos quando possível
    - Sem especulações
    Se não souber algo, admita claramente.
    """
    
    # Pergunta de teste
    PROMPT = "Explique o que é Docker e seus principais benefícios"
    
    # Testando diferentes métodos
    print("\nUsando requests:")
    print(consulta_ollama_requests(PROMPT, MODELO, HOST, MEU_PROMPT_SISTEMA))
    
    print("\nUsando LangChain:")
    print(consulta_langchain(PROMPT, MODELO, HOST, MEU_PROMPT_SISTEMA))
    
    print("\nUsando LiteLLM:")
    print(consulta_litellm(PROMPT, MODELO, HOST, MEU_PROMPT_SISTEMA))
    
    print("\nUsando HTTPx:")
    print(consulta_httpx(PROMPT, MODELO, HOST, MEU_PROMPT_SISTEMA))
    
    print("\nUsando aiohttp:")
    print(asyncio.run(consulta_aiohttp(PROMPT, MODELO, HOST, MEU_PROMPT_SISTEMA)))
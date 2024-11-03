# Usando LiteLLM 
# Uniformiza a interface com diferentes LLMs 
# Mais leve que o LangChain
# Requer: pip install litellm
from litellm import completion

def consulta_litellm(prompt, modelo, host):
    """
    Consulta usando LiteLLM
    """
    response = completion(
        model=f"ollama/{modelo}",
        messages=[{"role": "user", "content": prompt}],
        api_base=host
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    HOST = "http://192.168.0.190:11434"
    PROMPT = "Qual é a capital do Brasil?"
    MODELO = "llama3.2"
    
    # Usando LiteLLM
    print("\nResposta usando LiteLLM:")
    resposta2 = consulta_litellm(PROMPT, MODELO, HOST)
    print(resposta2)
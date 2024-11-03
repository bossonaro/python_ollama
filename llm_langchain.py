# Usando LangChain
# Framework mais completo para trabalhar com LLMs
# Oferece muitas funcionalidades extras como chains, agents e prompts templates
# Boa escolha se você planeja construir aplicações mais complexas
# Requer: pip install langchain langchain-community
from langchain_community.llms import Ollama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

def consulta_langchain(prompt, modelo, host):
    """
    Consulta usando LangChain
    """
    llm = Ollama(
        base_url=host,
        model=modelo,
        callbacks=[StreamingStdOutCallbackHandler()]
    )
    return llm.invoke(prompt)

# Exemplo de uso
if __name__ == "__main__":
    HOST = "http://192.168.0.190:11434"
    PROMPT = "Qual é a capital do Brasil?"
    MODELO = "llama3.2"
    
    # Usando LangChain
    print("\nResposta usando LangChain:")
    resposta1 = consulta_langchain(PROMPT, MODELO, HOST)
    print(resposta1)
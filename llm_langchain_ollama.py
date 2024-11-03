# Usando langchain_ollama
# Requer: pip install -U langchain-ollama

from langchain_ollama import OllamaLLM
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

def consulta_langchain(prompt, modelo, host):
    llm = OllamaLLM(
        base_url=host,
        model=modelo,
        callbacks=[StreamingStdOutCallbackHandler()]
    )
    return llm.invoke(prompt)

if __name__ == "__main__":
    HOST = "http://192.168.0.190:11434"
    PROMPT = "Qual é a capital do Brasil?"
    MODELO = "llama3.2"
    
    print("\nResposta usando LangChain:")
    resposta1 = consulta_langchain(PROMPT, MODELO, HOST)
    print(resposta1)

# Usando a biblioteca ollama-python
# Biblioteca oficial/wrapper para Python
# Interface mais amigável
# Suporte a mais funcionalidades específicas do Ollama
# Requer: pip install requests ollama-python
import requests
import json
from ollama_python.endpoints import GenerateAPI
from ollama_python import exceptions

def consulta_ollama_client(prompt, modelo, host):
    api = GenerateAPI(base_url=host, model=modelo)
    
    try:
        result = api.generate(prompt=prompt, options={}, format="json")
        
        # Se a resposta não contém os campos esperados, retorne um aviso
        if not hasattr(result, 'response'):
            return {"error": "Resposta da API não contém a chave 'response'."}
        
        return result.response

    except exceptions.HTTPError as e:
        return {"error": f"Erro de HTTP: {e}"}
    except exceptions.ValidationError as e:
        return {"error": f"Erro de validação: {e}"}
    except Exception as e:
        return {"error": f"Erro inesperado: {e}"}

# Exemplo de uso
if __name__ == "__main__":
    HOST = "http://192.168.0.190:11434"
    PROMPT = "Qual é a capital do Brasil?"
    MODELO = "llama3.2"
    
    print("\nResposta usando ollama-python:")
    resposta2 = consulta_ollama_client(PROMPT, MODELO, HOST)
    print(resposta2)
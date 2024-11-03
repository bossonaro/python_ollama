import warnings
from elasticsearch import Elasticsearch, ElasticsearchWarning
import requests

# Ignora avisos de segurança do Elasticsearch
warnings.filterwarnings("ignore", category=ElasticsearchWarning)

class ElasticLLMAssistant:
    def __init__(self, elastic_host, ollama_host, modelo):
        self.es = Elasticsearch([elastic_host])
        self.ollama_host = ollama_host
        self.modelo = modelo
        self.index_name = None
        self.mapping = None

    def list_indices(self):
        """
        Lista todos os índices disponíveis no Elasticsearch.
        """
        indices = self.es.cat.indices(format="json")
        return [(index['index'], idx) for idx, index in enumerate(indices)]

    def select_index(self):
        """
        Permite ao usuário selecionar um índice.
        """
        indices = self.list_indices()
        print("Índices disponíveis:")
        for name, idx in indices:
            print(f"{idx + 1}. {name}")

        choice = input("Digite o número ou nome do índice que deseja trabalhar: ")
        if choice.isdigit():
            self.index_name = indices[int(choice) - 1][0]
        else:
            self.index_name = choice

        print(f"Você selecionou o índice: {self.index_name}")
        self.mapping = self.es.indices.get_mapping(index=self.index_name)
        self.show_fields()

    def show_fields(self):
        """
        Mostra os campos e tipos de dados do índice selecionado.
        """
        fields = self.mapping[self.index_name]['mappings']['properties']
        print("Campos e tipos de dados:")
        for field, details in fields.items():
            print(f"Campo: {field}, Tipo: {details['type']}")

    def query_elasticsearch(self, question):
        """
        Faz uma consulta ao Elasticsearch com base na pergunta do usuário.
        """
        # Aqui você pode implementar lógica para criar uma consulta com base na pergunta
        # Por exemplo, utilizando o match query para encontrar correspondências
        search_body = {
            "query": {
                "match": {
                    "content": question  # Ajuste "content" para o campo relevante
                }
            }
        }
        response = self.es.search(index=self.index_name, body=search_body)
        return response['hits']['hits']

    def ask(self, question):
        """
        Faz uma pergunta ao LLM sobre os dados do índice.
        """
        # Consulta ao Elasticsearch
        search_results = self.query_elasticsearch(question)

        # Formata os resultados para o LLM
        if search_results:
            documents = "\n".join([f"ID: {doc['_id']}, Source: {doc['_source']}" for doc in search_results])
        else:
            documents = "Nenhum resultado encontrado."

        prompt = f"""
        Você é um assistente especializado em análise de dados do Elasticsearch.

        Aqui estão os documentos encontrados relacionados à sua pergunta:
        {documents}

        PERGUNTA: {question}
        
        Por favor, analise a pergunta considerando o índice '{self.index_name}' e os dados acima.
        """
        
        # Faz a requisição ao Ollama
        url = f"{self.ollama_host}/api/generate"
        payload = {
            "model": self.modelo,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                return response.json()['response']
            else:
                return f"Erro na chamada ao LLM: {response.status_code}"
        except Exception as e:
            return f"Erro: {str(e)}"

    def run(self):
        """
        Executa o assistente.
        """
        self.select_index()
        while True:
            question = input("\nDigite sua pergunta (ou 'sair' para encerrar): ")
            if question.lower() == 'sair':
                print("Encerrando...")
                break
            answer = self.ask(question)
            print("Resposta:", answer)

# Exemplo de uso
if __name__ == "__main__":
    ELASTIC_HOST = "http://192.168.0.40:9200"  # Ajuste conforme necessário
    OLLAMA_HOST = "http://192.168.0.190:11434"  # Ajuste conforme necessário
    MODELO = "llama3.2"
    
    # Inicializa o assistente
    assistant = ElasticLLMAssistant(ELASTIC_HOST, OLLAMA_HOST, MODELO)
    
    # Executa o assistente
    assistant.run()

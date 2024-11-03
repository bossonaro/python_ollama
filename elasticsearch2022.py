from elasticsearch import Elasticsearch, ElasticsearchWarning
import requests
import json
import warnings

# Ignora avisos de segurança do Elasticsearch
warnings.filterwarnings("ignore", category=ElasticsearchWarning)

class ElasticLLMAssistant:
    def __init__(self, elastic_host, ollama_host, index_name, modelo):
        """
        Inicializa o assistente com as conexões necessárias
        """
        self.es = Elasticsearch([elastic_host])
        self.ollama_host = ollama_host
        self.index_name = index_name
        self.modelo = modelo
        self.mapping = None
        self.sample_docs = None
        self.context = self._build_initial_context()

    def _build_initial_context(self):
    # Constrói o contexto inicial com o mapping e exemplos de documentos
        # Obtém o mapping do índice
        self.mapping = self.es.indices.get_mapping(index=self.index_name)
        
        # Converte o mapping para um dicionário padrão
        mapping_dict = {index: details['mappings'] for index, details in self.mapping.items()}
        
        # Obtém uma amostra de documentos
        sample_response = self.es.search(
            index=self.index_name,
            body={
                "size": 3,
                "query": {"match_all": {}}
            }
        )
        self.sample_docs = [hit['_source'] for hit in sample_response['hits']['hits']]

        # Constrói o prompt de sistema com as informações do índice
        context = f"""
        Você é um assistente especializado em análise de dados do Elasticsearch.
        
        MAPPING DO ÍNDICE '{self.index_name}':
        {json.dumps(mapping_dict, indent=2)}
        
        EXEMPLOS DE DOCUMENTOS:
        {json.dumps(self.sample_docs, indent=2)}
        
        DIRETRIZES:
        - Use o mapping acima para entender a estrutura dos dados
        - Os exemplos de documentos mostram o formato real dos dados
        - Quando necessário, sugira queries Elasticsearch para obter as informações
        - Se uma pergunta não puder ser respondida com a estrutura disponível, explique por quê
        - Seja preciso nas referências aos campos e seus tipos
        - Se necessário mais dados para uma resposta completa, indique quais dados seriam necessários
        """
        return context


    def _get_field_stats(self, field_name):
        """
        Obtém estatísticas básicas de um campo numérico
        """
        try:
            stats = self.es.search(
                index=self.index_name,
                body={
                    "size": 0,
                    "aggs": {
                        "stats": {
                            "stats": {"field": field_name}
                        }
                    }
                }
            )
            return stats['aggregations']['stats']
        except Exception as e:
            return f"Erro ao obter estatísticas: {str(e)}"

    def _execute_query(self, query):
        """
        Executa uma query no Elasticsearch
        """
        try:
            response = self.es.search(index=self.index_name, body=query)
            return response
        except Exception as e:
            return f"Erro na query: {str(e)}"

    def ask(self, question):
        """
        Faz uma pergunta ao LLM sobre os dados do índice
        """
        # Prepara o prompt completo
        prompt = f"""
        {self.context}
        
        PERGUNTA: {question}
        
        Por favor, analise a pergunta considerando o mapping e os exemplos fornecidos.
        Se necessário, sugira uma query Elasticsearch apropriada.
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

    def execute_and_analyze(self, question):
        """
        Faz uma pergunta, executa queries sugeridas e analisa os resultados
        """
        # Primeira interação: pede sugestão de query
        initial_response = self.ask(f"""
        {question}
        
        Por favor, sugira uma query Elasticsearch apropriada para responder esta pergunta.
        Retorne apenas a query em formato JSON, sem explicações adicionais.
        """)
        
        try:
            # Tenta extrair e executar a query sugerida
            query = json.loads(initial_response)
            query_result = self._execute_query(query)
            
            # Segunda interação: análise dos resultados
            analysis_prompt = f"""
            {self.context}
            
            PERGUNTA ORIGINAL: {question}
            
            RESULTADOS DA QUERY:
            {json.dumps(query_result, indent=2)}
            
            Por favor, analise os resultados e forneça uma resposta completa à pergunta original.
            """
            
            # Faz a análise final com o LLM
            final_analysis = self.ask(analysis_prompt)
            return final_analysis
            
        except json.JSONDecodeError:
            return f"Não foi possível extrair uma query válida da resposta do LLM: {initial_response}"
        except Exception as e:
            return f"Erro durante a execução: {str(e)}"

# Exemplo de uso
if __name__ == "__main__":
    # Configurações
    ELASTIC_HOST = "http://192.168.0.40:9200"
    OLLAMA_HOST = "http://192.168.0.190:11434"
    MODELO = "llama3.2"
    INDEX_NAME = "tse_2022_2"
    
    # Inicializa o assistente
    assistant = ElasticLLMAssistant(ELASTIC_HOST, OLLAMA_HOST, INDEX_NAME, MODELO)
    
    # Exemplo de perguntas
    perguntas = [
        "Quais campos existem neste índice?",
        "Que tipos de dados estão armazenados em cada campo?",
        "Pode me mostrar um exemplo de documento deste índice?"
    ]
    
    # Testa as perguntas
    for pergunta in perguntas:
        print(f"\nPergunta: {pergunta}")
        print("Resposta:", assistant.ask(pergunta))
        print("\nAnálise completa com execução de query:")
        print(assistant.execute_and_analyze(pergunta))
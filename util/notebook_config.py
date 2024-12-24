if 'config' not in locals():
    config = {}


config['AZURE_ENDPOINT'] = 'https://test-vm-eu2.openai.azure.com/'
config['chunk_size'] = 1000
config['chunk_overlap'] = 50
config['StorageContainerName'] = 'e2e-rag-msft-data-storage'
config['EMBEDDINGS_API_VERSION'] = '2023-05-15'
config['SEARCH_SERVICE_NAME']='azure-ai-rag-search-service'
config['SEARCH_INDEX_NAME']='msft-earnings-index'
config['vector_search_profile_name'] = 'myHnswProfile'
config['hnsw_algorithm_name'] = 'msft-earnings-index-hnsw'
config['azure-search-endpoint'] = 'https://azure-ai-rag-search-service.search.windows.net'
config['system_message_template'] = """You are a helpful assistant. You are good at helping to answer a question based on the context provided
If the context does not provide enough relevant information to determine the answer, just say I don't know. 
If the context is irrelevant to the question, just say I don't know. 
If you did not find a good answer from the context, just say I don't know. 
If the query doesn't form a complete question, just say I don't know. 
If there is a good answer from the context, try to summarize the context to answer the question."""

config['human_message_template'] = """Given the context: {context}. Answer the question {question}."""

config['LANGFUSE_SECRET_KEY'] = "sk-lf-5e1d3d5d-ae7d-417b-bba7-9303f3df3677"
config['LANGFUSE_PUBLIC_KEY'] = "pk-lf-db864f15-8401-42b7-b84d-ee1057d594ec"
config['Langfuse_host'] = "https://cloud.langfuse.com"

print ('The config is set up successfully!')

if 'config' not in locals():
    config = {}


config['AZURE_ENDPOINT'] = 'https://test-vm-eu2.openai.azure.com/'
config['chunk_size'] = 1000
config['chunk_overlap'] = 50
config['StorageConnectionString'] = 'DefaultEndpointsProtocol=https;AccountName=e2eragpipeline7232225101;AccountKey=5GIqE1eaQZxS6VZ3YGdwDIqULim9+PnIFajMJ2w7Q6P/kr3/jmExmnox9xMvtH/xpe87HNAbi1yX+ASttH0O2g==;EndpointSuffix=core.windows.net'
config['StorageContainerName'] = 'e2e-rag-msft-data-storage'
config['OPENAI_API_KEY'] ='EJdGQVCwEE9zlPiwFRolJqAUrQPyHWPIwonxf4NpJVpfDpN4SmwJJQQJ99AKACHYHv6XJ3w3AAABACOGY1DY'
config['EMBEDDINGS_API_VERSION'] = '2023-05-15'
config['OPENAI_KEY'] = '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'
config['SEARCH_SERVICE_NAME']='azure-ai-rag-search-service'
config['SEARCH_ADMIN_KEY']='agGSP1FWpW088LIRMutdd0excFBoIZvJjpkXQYeRZSAzSeCHLk6Z'
config['SEARCH_INDEX_NAME']='msft-earnings-index'
config['vector_search_profile_name'] = 'myHnswProfile'
config['hnsw_algorithm_name'] = 'msft-earnings-index-hnsw'

print ('The config is set up successfully!')


from azure.search.documents.indexes.models import (
    SimpleField,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
    SearchIndex,
    FreshnessScoringFunction,
    FreshnessScoringParameters,
    ScoringProfile,
    TextWeights
)

from langchain_community.vectorstores import AzureSearch
from langchain_openai import AzureOpenAI,AzureOpenAIEmbeddings
from langchain.schema import Document

from util.notebook_config import config
index_name = config['SEARCH_INDEX_NAME']

fields = [
    SimpleField(
        name="id",
        type=SearchFieldDataType.String,
        key=True,
        filterable=True,
    ),
    SearchableField(
        name="content",
        type = SearchFieldDataType.String,
        searchable=True
    ),
    SearchField(
        name = "content_vector",
        type = SearchFieldDataType.Collection(SearchFieldDataType.Single),
        searchable=True,
        vector_search_dimensions=1536,
        vector_search_profile_name=config['vector_search_profile_name'],
    ),
    SearchableField(
        name="metadata",
        type=SearchFieldDataType.String,
        searchable=True,
    ),
    # Additional field for filtering on document source
    SimpleField(
        name="source",
        type=SearchFieldDataType.String,
        filterable=True,
    ),

    SimpleField(
        name="last_update",
        type=SearchFieldDataType.DateTimeOffset,
        searchable=True,
        filterable=True,
    ),

]

sc_name = "scoring_profile"
sc = ScoringProfile(
    name=sc_name,
    text_weights=TextWeights(weights={"content": 5}),
    function_aggregation="sum",
    functions=[
        FreshnessScoringFunction(
            field_name="last_update",
            boost=100,
            parameters=FreshnessScoringParameters(boosting_duration="P2D"),
            interpolation="linear",
        )
    ],
)

api_key = config['OPENAI_API_KEY']
api_version = config['EMBEDDINGS_API_VERSION']
azure_endpoint = config['AZURE_ENDPOINT']

embeddings = AzureOpenAIEmbeddings(
    model="text-embedding-3-small",
    api_version=api_version,
    azure_endpoint=azure_endpoint,
    api_key=api_key
    )


vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name=config['hnsw_algorithm_name'])],
        profiles=[
            VectorSearchProfile(
                name=config['vector_search_profile_name'],
                algorithm_configuration_name=config['hnsw_algorithm_name'],
            )
        ],
    )

index_name = "earning_call-scoring-profile"
vector_store: AzureSearch = AzureSearch(
    azure_search_endpoint='https://azure-ai-rag-search-service.search.windows.net',
    azure_search_key=config['SEARCH_ADMIN_KEY'],
    index_name=index_name,
    embedding_function=embeddings.embed_query,
    fields=fields,
    scoring_profiles=[sc],
    default_scoring_profile=sc_name,
    vector_search=vector_search
)

import json

file_path = 'data\MSFT-earnings-inout-data.json'
with open (file_path, 'r', encoding='utf-8') as file:
    json_data = json.load(file)

def json_to_documents(json_data):
    documents = [
        Document(page_content=doc["content"], metadata=doc["metadata"])  # Convert each dict back to Document
        for doc in json_data
    ]
    return documents

documents = json_to_documents(json_data)
vector_store.add_documents(documents)


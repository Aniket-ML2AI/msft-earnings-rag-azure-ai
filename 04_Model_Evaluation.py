from langchain_openai import ChatOpenAI,AzureOpenAIEmbeddings
import ragas.testset
from util.notebook_config import config
from ragas.testset import TestsetGenerator
import json
from langchain.schema import Document
from ragas.testset.synthesizers import default_query_distribution
import nest_asyncio
nest_asyncio.apply()



llm = ChatOpenAI(api_key=config['OPENAI_KEY'],
             model="gpt-4o-mini",
             temperature=0.5,
             max_tokens=400
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


generator = TestsetGenerator.from_langchain(
    llm = llm,
    embedding_model=embeddings

)

file_path = 'data\MSFT-earnings-inout-data.json'
with open (file_path, 'r', encoding='utf-8') as file:
    json_data = json.load(file)

def json_to_documents(json_data):
    documents = []
    for doc in json_data:
        documents.append(Document(page_content=doc["content"], metadata=doc["metadata"]))

    return documents

documents = json_to_documents(json_data)

testset = generator.generate_with_langchain_docs(documents,testset_size=10)
testset.to_pandas().to_excel('data/Ground_Truth_Dataset.xlsx',index=False)
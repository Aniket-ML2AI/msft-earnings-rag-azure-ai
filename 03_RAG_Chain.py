from util.notebook_config import config
from langchain.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings,ChatOpenAI
from langchain import LLMChain
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from azure.search.documents.models import VectorizedQuery
import warnings
from dotenv import load_dotenv
load_dotenv()
warnings.filterwarnings("ignore")
from langfuse import Langfuse
from langfuse.callback import CallbackHandler


api_key = config['OPENAI_API_KEY']
api_version = config['EMBEDDINGS_API_VERSION']
azure_endpoint = config['AZURE_ENDPOINT']

embeddings = AzureOpenAIEmbeddings(
    model="text-embedding-3-small",
    api_version=api_version,
    azure_endpoint=azure_endpoint,
    api_key=api_key
    )

vectorStore = AzureSearch(
    azure_search_endpoint=config['azure-search-endpoint'],
    embedding_function=embeddings.embed_query,
    index_name=config['SEARCH_INDEX_NAME'],
    azure_search_key = config['SEARCH_ADMIN_KEY']
    )


def hybrid_search(query, top=3):
    """Perform a hybrid search (combination of full-text and vector search)."""
    embedded_query = embeddings.embed_query(query)
    vector_query = VectorizedQuery(vector=embedded_query, k_nearest_neighbors=5, fields="content_vector")
    results = vectorStore.client.search(
        search_text=query,
        vector_queries=[vector_query],
        filter = "source eq 'data\\MSFT_q1_2024.txt'",
        top=top,
    )
    return list(results)

#azure_ai_retriever = vectorStore.as_retriever()
query = "How is Windows OEM revenue growth in Q1?"
#azure_ai_retriever.search_kwargs["filters"] = "source eq 'data\\MSFT_q1_2024.txt'"

docs = hybrid_search(query)


system_message_prompt = SystemMessagePromptTemplate.from_template(config['system_message_template'])
human_message_prompt = HumanMessagePromptTemplate.from_template(config['human_message_template'])
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt,human_message_prompt])

llm = ChatOpenAI(api_key=config['OPENAI_KEY'],
             model="gpt-4o-mini",
             temperature=0.5,
             max_tokens=400
                  )

qa_chain = LLMChain(
    llm=llm,
    prompt=chat_prompt
)
context = "\n".join(doc['content'] for doc in docs)

langfuse_handler = CallbackHandler()
response = qa_chain.invoke({"context":context,"question":query},config={"callbacks": [langfuse_handler]})

   
import warnings
warnings.filterwarnings("ignore")
from util.notebook_config import config
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from datetime import datetime,timedelta
from util.logger import logging
import json
from azure.storage.blob import BlobServiceClient,BlobClient,ContainerClient, ContentSettings
import uuid
import re

def split_doc(filename_):
    print (f'Reading - {filename_}')
    loader = TextLoader(filename_,encoding='utf-8')
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size = config['chunk_size'],chunk_overlap=config['chunk_overlap'])
    docs = text_splitter.split_documents(documents)
    return docs

def add_metadata(data,time):
    for chunk in data:
        chunk.metadata['last_update'] = time
    return data

def add_ids(data):
    for index, chunk in enumerate(data):
        match = re.search(r"\\([^\\]+)\.",chunk.metadata['source'])
        if match:
            chunk.metadata['id'] = f"doc-{index+1}-{match.group(1)}"
    return data

q2_time = (datetime.utcnow() - timedelta(days=90)).strftime("%Y-%m-%dT%H:%M:%S-00:00")
q1_time = (datetime.utcnow() - timedelta(days=180)).strftime("%Y-%m-%dT%H:%M:%S-00:00")

msft_q1 = split_doc('data\MSFT_q1_2024.txt')
msft_q2 = split_doc('data\MSFT_q2_2024.txt')

msft_q1 = add_metadata(msft_q1,q1_time)
msft_q2 = add_metadata(msft_q2,q2_time)

msft_q1 = add_ids(msft_q1)
msft_q2 = add_ids(msft_q2)

documents = msft_q1+msft_q2

print (type(documents))

logging.info('This is combined document for q1+q2')
logging.info(documents)

def document_to_json(documents):
    document_list = []
    for doc in documents:
        doc_dict = {
            "metadata":doc.metadata,
            "content":doc.page_content
        }
        document_list.append(doc_dict)
    
    return json.dumps(document_list)



def upload_to_Blob(data):
    blob_service_client = BlobServiceClient.from_connection_string(config['StorageConnectionString'])
    container_client = blob_service_client.get_container_client(config['StorageContainerName'])
    blob_name = "MSFT-earnings-inout-data.json"
    blob_client = container_client.get_blob_client(blob_name)
    content_settings = ContentSettings(content_type="application/json")
    blob_client.upload_blob(
        data,
        overwrite=True,
        content_settings=content_settings
        )
    logging.info(f"File {blob_name} is successfully added to {config['StorageContainerName']}")


json_data = document_to_json(documents)
upload_to_Blob(json_data)






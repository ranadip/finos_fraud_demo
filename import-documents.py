from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
import os

import logging
logging.basicConfig(level=logging.INFO)
logging.debug("test")

DEFAULT_MODEL="gemini-2.0-flash-001"
embedding_model_name = "text-embedding-004"
API_KEY=os.environ.get("GOOGLE_API_KEY")

llm = GoogleGenAI(model=DEFAULT_MODEL,api_key=API_KEY)
Settings.llm = llm
Settings.embed_model = GoogleGenAIEmbedding(model_name=embedding_model_name, api_key=API_KEY)

documents = SimpleDirectoryReader("./raw_docs").load_data()
index = VectorStoreIndex.from_documents(documents)
index.storage_context.persist(persist_dir="_index")
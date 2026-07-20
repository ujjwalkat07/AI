from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

loader = PyPDFLoader("RAG/ujjwal-resume.pdf")
documents = loader.load()


text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
texts = text_splitter.split_documents(documents)

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")


vector_store = Chroma(
    collection_name="rag-collection",
    embedding_function=embeddings,
    persist_directory="chroma-db"
)
vector_store.add_documents(documents=texts)
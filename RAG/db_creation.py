from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

load_dotenv()

# 1. Load
# load document from pdf file and print the content of the first page of the document.
# pdf_path = Path(__file__).resolve().parent / "ujjwal-resume.pdf"
loader = PyPDFLoader("RAG/ujjwal-resume.pdf")
documents = loader.load()
# print(documents[0].page_content)


# 2. Split
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
texts = text_splitter.split_documents(documents)
# print(f"Number of documents: {texts[0]}")
# print(f"Number of chunks: {len(texts)}")


# 3. Generate embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")

vector_store = Chroma(
    collection_name="rag-collection",
    embedding_function=embeddings,
    persist_directory="chroma-db",
)
vector_store.add_documents(documents=texts)

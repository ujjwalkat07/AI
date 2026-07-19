from pathlib import Path
from langchain_core import documents
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
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
# vector = embeddings.embed_query(texts[0].page_content)
# print(f"Embedding vector: {vector}")

# 4. Store in vector database
# Here we are using Chroma as the vector database to store the embeddings. We are creating
vector_store = Chroma(
    collection_name="rag-collection",
    embedding_function=embeddings,
    persist_directory="chroma-db"
)
vector_store.add_documents(documents=texts)

# 5. Query/ Retrieve the documents from the vector database using a query. Here we are using the similarity_search method of the vector store to retrieve the documents that are similar to the query. The k parameter specifies the number of documents to retrieve.
results = vector_store.similarity_search(
    "what is the name of the person in the resume?",
    k=2,
)

print(f"Number of results: {results}")
model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")

# set the prompt template for the model to use. The template consists of a system message and a human message. The system message is used to set the context for the model, while the human message is used to provide the user's input.

template = ChatPromptTemplate(
    [
        (
            "system",
            "You are a helpful AI bot. and you are given a document to answer questions about it. The document is as follows: {document}",
        ),
        ("human", "{user_input}"),
    ]
)
# for asking question here we used invoke method of the model object and passed the question as a string argument to it.
while True:
    val = input("Enter your question: ")
    test_prompt = template.format_messages(
        document=documents[0].page_content, user_input=val
    )

    # passes to AI model and get the response
    response = model.invoke(test_prompt)
    # Capture the content of the response
    content = response.content
    print(content[0].get("text"))
    print("\n\n")

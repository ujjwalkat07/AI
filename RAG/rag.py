from pathlib import Path
from langchain_core import documents
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

load_dotenv()


# 1. Generate embeddings for user query
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")
# vector = embeddings.embed_query(texts[0].page_content)
# print(f"Embedding vector: {vector}")

# 4. Retrieve from vector database
# Here we are using Chroma as the vector database to store the embeddings. We are creating
vector_store = Chroma(
    collection_name="rag-collection",
    embedding_function=embeddings,
    persist_directory="chroma-db",
)

# 5. Query/ Retrieve the documents from the vector database using a query. Here we are using the similarity_search method of the vector store to retrieve the documents that are similar to the query. The k parameter specifies the number of documents to retrieve.

# query again gets split into embeddings means again AI API COST
# results = vector_store.similarity_search(
#     "what is the skills of the person in the resume?",
#     k=2,
# )

retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 4, "fetch_k": 20, "lambda_mult": 0.5},
)

# print(f"Number of results: {retriever}")
model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")

# set the prompt template for the model to use. The template consists of a system message and a human message. The system message is used to set the context for the model, while the human message is used to provide the user's input.

template = ChatPromptTemplate(
    [
        (
            "system",
            """
              You are a helpful AI bot. use only provided content to answer the question. If the answer is not present in the content, say 'I don't know'.
            """,
        ),
        (
            "human",
            """
Context: {context}
Question: {user_input}
""",
        ),
    ]
)
# for asking question here we used invoke method of the model object and passed the question as a string argument to it.
while True:
    question = input("Enter your question: ")

    documents = retriever.invoke(question)
    # Use ALL retrieved chunks, not just the first one and make a list of chunks to pass to the prompt template. The context is created by joining the page content of all the retrieved documents with a separator.
    context = "\n\n---\n\n".join(doc.page_content for doc in documents)
    print(f"Retrieved {len(documents)} documents for the question: '{question}'")
    print(f"Context: {context}\n\n")

    final_prompt = template.format_prompt(context=context, user_input=question)

    # passes to AI model and get the response
    response = model.invoke(final_prompt)
    # Capture the content of the response
    content = response.content
    print(content[0].get("text"))
    print("\n\n")

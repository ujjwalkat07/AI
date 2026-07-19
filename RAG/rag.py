from pathlib import Path
from langchain_core import documents
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# 1. Load
# load document from pdf file and print the content of the first page of the document.
# pdf_path = Path(__file__).resolve().parent / "ujjwal-resume.pdf"
loader = PyPDFLoader("RAG/ujjwal-resume.pdf")
documents = loader.load()
# print(documents[0].page_content)

# 2. Split
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
texts = text_splitter.split_documents(documents)

# 3. Generate embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")
vector = embeddings.embed_query("hello, world!")
vector[:5]



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

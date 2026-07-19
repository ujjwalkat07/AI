# import os
from pathlib import Path

from langchain_core import documents
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

# load document from pdf file and print the content of the first page of the document.
pdf_path = Path(__file__).resolve().parent / "ujjwal-resume.pdf"
loader = PyPDFLoader(str(pdf_path))
documents = loader.load()
# print(documents[0].page_content)

model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")

# set the prompt template for the model to use. The template consists of a system message and a human message. The system message is used to set the context for the model, while the human message is used to provide the user's input.

template = ChatPromptTemplate(
        [
            ("system", "You are a helpful AI bot. and you are given a document to answer questions about it. The document is as follows: {document}"),
            ("human", "{user_input}"),
        ]
    )
# for asking question here we used invoke method of the model object and passed the question as a string argument to it.
while True:
    val = input("Enter your question: ")
    prompt_value = template.invoke(
        {
            "document": documents[0].page_content,
            "user_input": val,
        }
    )
    response = model.invoke(prompt_value)
    # Capture the content of the response
    content = response.content
    print(content[0].get("text"))
    print("\n\n")
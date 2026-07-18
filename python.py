# import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")

# for asking question here we used invoke method of the model object and passed the question as a string argument to it.
while True:
    prompt = input("Enter your question: ")
    response = model.invoke(prompt)
    # Capture the content of the response
    content = response.content
    # Write the content to a file named "read.md" in append mode with UTF-8 encoding
    with open("read.md", "+a", encoding='utf-8') as f:
        f.write(content[0].get("text"))

    print(content[0].get("text"))
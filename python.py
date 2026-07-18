import os
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["GOOGLE_API_KEY"] = "AIzaSyAwZ8ztwQmMuQuxWVYflBx2u-3VMWu1t9k"

model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")
response = model.invoke("write a python code for building AI agent that automate emails and also tell me the usage of it.")

content = response.content
if isinstance(content, list):
    text = "".join(block["text"] for block in content if isinstance(block, dict) and "text" in block)
else:
    text = content

with open("read.md", "w", encoding='utf-8') as f:
    f.write(text)
print(text)
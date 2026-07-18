# import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")
response = model.invoke("Tell me about yourself in 100 words.")

content = response.content
    # if isinstance(content, list):
    #     text = "".join(block["text"] for block in content if isinstance(block, dict) and "text" in block)
    # else:
    #     text = content

with open("read.md", "w", encoding='utf-8') as f:
    f.write(content[0].get("text"))
print(content[0].get("text"))
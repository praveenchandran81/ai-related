from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

model = ChatGoogleGenerativeAI(model="gemini-3.8-flash")

chat_template = ChatPromptTemplate([
    {"role": "system", "content": "You are a helpful customer support agent"},
    MessagesPlaceholder(variable_name="chat_history"),
    {"role": "user", "content": "{query}"}
])

#load chat history from a file or database
chat_history = []

with open("chat_history.txt", "r") as file:
    chat_history.extend(file.readlines())

prompt = chat_template.invoke({"query": "where is my refund?", "chat_history": chat_history})

result = model.invoke(prompt)

print(f"AI: {result.content[0]['text']}")

 
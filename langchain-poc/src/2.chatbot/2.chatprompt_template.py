from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

model = ChatGoogleGenerativeAI(model="gemini-3.8-flash")

chat_template = ChatPromptTemplate([
    {"role": "system", "content": "You are a helpful assistant in {domain}"},
    {"role": "user", "content": "Give me a brief overview of {topic}."}
])

prompt = chat_template.invoke({"domain": "technology", "topic": "artificial intelligence"})

result = model.invoke(prompt)

print(f"AI: {result.content[0]['text']}")


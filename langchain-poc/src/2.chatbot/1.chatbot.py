from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

model = ChatGoogleGenerativeAI(model="gemini-3.8-flash")

chat_history = [
    SystemMessage(content="You are a helpful assistant."),
   # HumanMessage(content="Hello! How are you?"),
   # AIMessage(content="I'm doing well, thank you! How can I assist you today?"),
]

while True:
    user_input= input("You:")
    chat_history.append(HumanMessage(content=user_input))
    if(user_input.lower() in ["exit", "quit"]):
        print("Exiting the chat. Goodbye!")
        break
    result = model.invoke(chat_history)
    chat_history.append(AIMessage(content=result.content))
    print(f"AI: {result.content[0]['text']}")

print("chat_history:", chat_history)
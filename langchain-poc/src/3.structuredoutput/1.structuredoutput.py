from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

model = ChatGoogleGenerativeAI(model="gemini-3.8-flash")

#schema
class Review(TypedDict):
    summary: str
    sentiment: str

structured_model = model.with_structured_output(Review)

prompt = "The product was very poor in quality and very expensive. I am very disappointed with my purchase."

result = structured_model.invoke(prompt)

print(f"Summary: {result['summary']}")
print(f"Sentiment: {result['sentiment']}")  


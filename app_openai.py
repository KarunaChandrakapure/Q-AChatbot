import openai
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os

from dotenv import load_dotenv
load_dotenv()

os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACKING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]="Simple Q&A Chatbot With OPENAI"


## Prompt Template

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assisant. Please reponse to user queries"),
        ("user","Question:{question}")
    ]
)

def generate_response(question,api_key,engine,temperature,max_tokens):
    openai.api_key=api_key
    llm=ChatOpenAI(model=engine)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    answer=chain.invoke({'question':question})
    return answer

st.title("Enhanced Q&A chatbot with OpenAI")
st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Enter your Open AI API KEY:",type="password")

engine=st.sidebar.selectbox("Select Open AI model",["gpt-4o","gpt-4-turbo","gpt-4"])
temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens=st.sidebar.slider("Max Tokens",min_value=50,max_value=300,value=150)

st.write("How can I help you Today ?")
user_input=st.text_input("You:")

if user_input and api_key:
    response = generate_response(user_input,api_key,engine,temperature,max_tokens)
    st.write(response)
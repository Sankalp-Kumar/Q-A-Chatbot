import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os 
from dotenv import load_dotenv
load_dotenv()

#langsmith tracking
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]= "Q&A Chatbot with Ollama and opensource models"

#Defining the prompt template

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant . Please  repsond to the user queries"),
        ("user","Question:{question}")
    ]
)


def generate_response(question,engine,temperature,max_tokens):


    llm = Ollama(model=engine)
    output_parser = StrOutputParser()
    chain = prompt|llm|output_parser
    answer = chain.invoke({"question":question})

    return answer


#Title of the app
st.title("Enhanced Q&A Chatbot With Open Source models")

## creating sidebar for different parameters
st.sidebar.title("Settings")

## Select the OpenAI model
engine=st.sidebar.selectbox("Please select the AI model",["mistral","phi3","llama3"])

## Adjust response parameter
temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)

## MAin interface for user input
st.write("Please ask your query")
user_input=st.text_input("You:")

if user_input:
    response = generate_response(user_input,engine,temperature,max_tokens)
    st.write(response)

else:
    st.write("Please provide the user input")


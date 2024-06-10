from langchain_openai import ChatOpenAI
from dotenv import load_dotenv 
import os 
import requests
from langsmith.wrappers import wrap_openai


#from langchain_core.tools import tool
# TODO: Transformarlo en una clase por cada modelo diferente
load_dotenv()
openai_model = os.getenv('OPENAI_MODEL')



chat_model = ChatOpenAI(model=openai_model, temperature=0)
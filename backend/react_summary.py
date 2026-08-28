import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from huggingface_hub import InferenceClient
from pydantic import BaseModel  # 1. Pydantic ko import kiya

# .env load
load_dotenv()
token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

app = FastAPI()

# React call
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hugging Face - Inference Client 
client = InferenceClient(model="facebook/bart-large-cnn", token=token)


class SummarizeRequest(BaseModel):
    text: str

@app.post("/summarize")
def summarize(data: SummarizeRequest): 
    response = client.summarization(data.text)
    
    
    return {"summary": response.summary_text}


""" 1. DOWNLOAD FAST API TERMINAL COMMAND: py -m pip install fastapi uvicorn
    2. TO RUN:py -m uvicorn react_summary:app --reload
    3. COPY THE LINK SHOWN IN TERMINAL: http://127.0.0.1:8000
                                        add  /docs in end
        proper link is to browse on goole is :http://127.0.0.1:8000/docs (don't copy it from here copy from terminal only)"""

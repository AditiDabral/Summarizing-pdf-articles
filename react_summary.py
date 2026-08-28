import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from huggingface_hub import InferenceClient
from pydantic import BaseModel  # 1. Pydantic ko import kiya

# .env फाइल से टोकन लोड करें
load_dotenv()
token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

app = FastAPI()

# React से कनेक्ट करने के लिए CORS इनेबल करें
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hugging Face का Inference Client सेट करें
client = InferenceClient(model="facebook/bart-large-cnn", token=token)

# 2. Pydantic Model banaya (Yahan define kiya ki request me kya aana chahiye)
class SummarizeRequest(BaseModel):
    text: str

@app.post("/summarize")
def summarize(data: SummarizeRequest):  # 3. yahan dict ki jagah Pydantic model ka use kiya
    # Ab data.text seedha access kar sakte hain
    response = client.summarization(data.text)
    
    # रिस्पांस से समरी निकालकर भेजना
    return {"summary": response.summary_text}


""" 1. DOWNLOAD FAST API TERMINAL COMMAND: py -m pip install fastapi uvicorn
    2. TO RUN:py -m uvicorn react_summary:app --reload
    3. COPY THE LINK SHOWN IN TERMINAL: http://127.0.0.1:8000
                                        add  /docs in end
        proper link is to browse on goole is :http://127.0.0.1:8000/docs (don't copy it from here copy from terminal only)"""
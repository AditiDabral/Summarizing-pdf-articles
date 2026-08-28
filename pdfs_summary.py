import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from huggingface_hub import InferenceClient
from pypdf import PdfReader  # PDF padhne ke liye

load_dotenv()
token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = InferenceClient(model="facebook/bart-large-cnn", token=token)


@app.post("/summarize-pdf")
async def summarize_pdf(file: UploadFile = File(...)):
  # 1. read pdf file
  reader = PdfReader(file.file)
  text = ""

  # 2. PDF pages  text extract 
  for page in reader.pages:
    extracted_text = page.extract_text()
    if extracted_text:
      text += extracted_text + "\n"

#text limit
  input_text = text[:4000]

  # 3. Hugging Face Inference Client 
  response = client.summarization(input_text)

  return {"filename": file.filename, "summary": response.summary_text}



"""downlod pdf write in terminal : py -m pip install pydf

 1. DOWNLOAD FAST API TERMINAL COMMAND: py -m pip install fastapi uvicorn
    2. TO RUN:py -m uvicorn react_summary:app --reload
    3. COPY THE LINK SHOWN IN TERMINAL: http://127.0.0.1:8000
                                        add  /docs in end
        proper link is to browse on goole is :http://127.0.0.1:8000/docs (don't copy it from here copy from terminal only)
"""
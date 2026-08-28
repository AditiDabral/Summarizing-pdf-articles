import os
from io import BytesIO

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from huggingface_hub import InferenceClient
from pypdf import PdfReader


# Load .env
load_dotenv()

token = os.getenv("HUGGINGFACEHUB_API_TOKEN")


# Create FastAPI app
app = FastAPI()


# Allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Hugging Face client
client = InferenceClient(
    model="facebook/bart-large-cnn",
    token=token
)


# PDF summarization endpoint
@app.post("/summarize")
async def summarize(file: UploadFile = File(...)):

    # Check file type
    if file.content_type != "application/pdf":
        return {
            "error": "Please upload a PDF file."
        }

    # Read uploaded PDF
    pdf_data = await file.read()

    # Read PDF directly from memory
    reader = PdfReader(BytesIO(pdf_data))

    # Extract text from all pages
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    # Check if text was extracted
    if not text.strip():
        return {
            "error": "Could not extract text from this PDF."
        }

    # Split text into smaller chunks
    chunk_size = 3000

    chunks = [
        text[i:i + chunk_size]
        for i in range(0, len(text), chunk_size)
    ]

    summaries = []

    # Summarize each chunk
    for chunk in chunks:

        response = client.summarization(chunk)

        summaries.append(response.summary_text)

    # Combine all summaries
    final_summary = " ".join(summaries)

    return {
        "summary": final_summary
    }
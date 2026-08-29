import os
import io
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from huggingface_hub import InferenceClient
from pypdf import PdfReader

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

# Initialize Hugging Face Client
client = InferenceClient(token=token)

@app.post("/summarize-pdf")
async def summarize_pdf(file: UploadFile = File(...)):
    print(f"\n--- Request aayi hai: {file.filename} ---")
    try:
        # 1. Read PDF file bytes safely
        contents = await file.read()
        reader = PdfReader(io.BytesIO(contents))
        text = ""

        # 2. Extract text from pages
        for i, page in enumerate(reader.pages):
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"

        print(f"Total extracted text length: {len(text)} characters")

        if not text.strip():
            raise HTTPException(status_code=400, detail="PDF ke andar koi text nahi mila!")

        # Limit text safely to avoid index error
        input_text = text[:1000]

        # 3. Call Hugging Face Model
        print("Hugging Face model ko request bhej rahe hain...")
        response = client.summarization(
            model="facebook/bart-large-cnn",
            text=input_text
        )

        # Safely extract summary text handling different return types
        if hasattr(response, "summary_text"):
            summary_text = response.summary_text
        elif isinstance(response, dict):
            summary_text = response.get("summary_text", str(response))
        else:
            summary_text = str(response)

        print("Summary successfully ban gayi!")

        return {"filename": file.filename, "summary": summary_text}

    except Exception as e:
        print(f"❌ KAHIN PAR ERROR AAYI HAI: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
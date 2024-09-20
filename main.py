from fastapi import FastAPI, File, UploadFile, HTTPException
from mindee import Client, PredictResponse, product
import io

# Initialize the FastAPI app
app = FastAPI(
    title="Receipt Extraction API",
    description="Gal ❤️Galo This API allows you to upload an image of a receipt (JPEG or PNG) and extracts the relevant data using Mindee's Receipt OCR.",
    version="1.0.0"
)

# Initialize Mindee client with your API key
mindee_client = Client(api_key="106c2fa10900bac0ec5e58816bbc55da")


@app.post("/extract-receipt/")
async def extract_receipt(file: UploadFile = File(...)):
    # Check if the file is an image
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG and PNG are allowed.")

    try:
        # Read the uploaded file
        contents = await file.read()

        # Use the Mindee client to parse the image
        input_doc = mindee_client.source_from_bytes(contents, filename=file.filename)
        result: PredictResponse = mindee_client.parse(product.ReceiptV5, input_doc)

        # Extract and return the parsed data
        extracted_data = result.document  # Convert result to dictionary

        return {"message": "Extraction successful", "data": extracted_data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting data: {e}")


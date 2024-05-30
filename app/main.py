from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv
from app.routes import donations, user, donor, recipient, reviews
from database import donor_collection, recipient_collection, donation_collection, user_collection, review_collection

load_dotenv()  # Load environment variables from .env file

# Create the FastAPI app instance
app = FastAPI(
    title="Food Donation API",
    description="API for managing food donations, users, donors, recipients, and reviews",
    version="1.0.0",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin, change in production
    allow_credentials=True,  # Allow cookies and authentication headers
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)

# Include routes from other modules
app.include_router(user.router)
app.include_router(donor.router)
app.include_router(donations.router)
app.include_router(recipient.router)
app.include_router(reviews.router)

# Africa's Talking SMS API credentials
AT_USERNAME = os.getenv("sustain")
AT_API_KEY = os.getenv("b0de5d6951164cd6387c3fcebbce1588163399d5ad1c08d00d0bd666088df386")
AT_SMS_URL = "https://api.africastalking.com/version1/messaging"

class SMSRequest(BaseModel):
    to: str
    message: str

@app.post("/send-sms/")
def send_sms(sms_request: SMSRequest):
    headers = {
        "apiKey": AT_API_KEY,
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }

    payload = {
        "username": AT_USERNAME,
        "to": sms_request.to,
        "message": sms_request.message,
    }

    response = requests.post(AT_SMS_URL, headers=headers, data=payload)

    if response.status_code == 201:
        return {"message": "SMS sent successfully"}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())


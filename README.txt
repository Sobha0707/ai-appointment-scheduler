# AI-Powered Appointment Scheduler Assistant

## Problem Statement

This Project implements a backend service that parse appointment requests both text and image inputs and converts them into structured scheduling data.

The System follows a pipeline:
OCR -> Entity Extraction -> Date/Time Normalization -> Final JSON Output

## Features 
- Accepts typed text input
- Accepts image input using OCR (Tesseract)
- Extracts department, date, and time
- Normalizes date/time to Asia/Kolkata timezone
- Implements guardrails for ambiguous inputs
- REST API built using Flask

## Tech Stack
- Python
- Flask
- Tesseract OCR
- Pillow
- Dtaeutil

## Project Structure

appointment_Task1/

|-----app.py
|------appointment_parser.py
|------requirements.txt
|-------README.md
|----test.png

-----


---

## Setup Instructions

### 1. Install Dependencies

pip install -r requirements.txt

2. Install Tesseract OCR (Windows)

Download and install form:

https://github.com/UB-Mannheim/tesseract/wiki

Ensure tesseract.exe is available in:

C:\Program Files\Tesseract-OCR\

Running the Application

 python app.py

The server will start at:
 
http://127.0.0.1:5000

API Usage

1. Parse Appointment from Text

curl -X POST http://127.0.0.1:5000/parse-appointment \
-H "Content-Type: application/json" \
-d "{\"text\":\"Book dentist next Friday at 3pm\"}"

Sample Response

{
  "appointment": {
    "department": "Dentist",
    "date": "2026-01-30",
    "time": "15:00",
    "tz": "Asia/Kolkata"
  },
  "status": "ok"
}

2. Parse Appointment from Image (OCR)

curl -X POST http://127.0.0.1:5000/parse-appointment-image \
-F "file=@test.png"

Sample Response
{
  "raw_text": "Book dentist next Friday at 3pm",
  "parsed_output": {
    "appointment": {
      "department": "Dentist",
      "date": "2026-01-30",
      "time": "15:00",
      "tz": "Asia/Kolkata"
    },
    "status": "ok"
  }
}

Guardrails

Missing or ambiguous date/time triggers needs_clarification

Empty or invalid inputs return appropriate error messages

OCR output is returned as raw_text for transparency






from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from flask import Flask, request, jsonify
from appointment_parser import process_text

app = Flask(__name__)

@app.route("/parse-appointment", methods=["POST"])
def parse_appointment():
    data = request.json

    if not data or "text" not in data:
        return jsonify({
            "status": "error",
            "message": "Missing 'text' field"
        }), 400

    result = process_text(data["text"])
    return jsonify(result)

@app.route("/parse-appointment-image", methods=["POST"])
def parse_appointment_image():
    if "file" not in request.files:
        return jsonify({
            "status": "error",
            "message": "No image file provided"
        }), 400

    file = request.files["file"]
    image = Image.open(file)

    extracted_text = pytesseract.image_to_string(image)
    result = process_text(extracted_text)

    return jsonify({
        "raw_text": extracted_text.strip(),
        "parsed_output": result
    })

if __name__ == "__main__":
    app.run(debug=True)

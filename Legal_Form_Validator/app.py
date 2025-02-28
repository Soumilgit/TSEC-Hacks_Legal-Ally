from flask import Flask, request, render_template, jsonify
import pdfplumber
import os

app = Flask(__name__)

# Expected fields for each form type
FORM_FIELDS = {
    "Advocate Form": [
        "Advocate Name",
        "Surname",
        "First Name",
        "Middle Name",
        "Sex",
        "Date of Birth",
        "Bar Registration Number",
    ],
    "Filing Form": [
        "District & Sessions Court",
        "Case Type",
        "Plaintiff Name",
        "Father/Mother/Husband Name",
        "Address",
        "Sex",
    ],
    "Litigant Form": [
        "Court Complex",
        "District",
        "Litigant Name",
        "Surname",
        "First Name",
        "Middle Name",
        "Mobile Number",
        "Email",
    ],
    "Vakalatnama Form": [
        "Court Name",
        "Suit/Appeal No",
        "Plaintiff(s) or Petitioner(s)",
        "Defendant(s) or Respondent(s)",
        "Advocate Signature",
        "Client Signature",
    ],
}

def extract_text_from_pdf(pdf_path):
    """Extract text from the uploaded PDF file."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
    return text.strip()

def find_missing_fields(extracted_text, expected_fields):
    """Identify missing fields from extracted text."""
    extracted_lines = set(extracted_text.split("\n"))

    # Identify missing fields
    missing_fields = [field for field in expected_fields if field not in extracted_lines]

    return missing_fields

@app.route("/")
def home():
    """Render the homepage."""
    return render_template("index.html")

@app.route("/compare", methods=["POST"])
def compare_pdf():
    """Handle PDF upload and comparison."""
    if "pdf-file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    pdf_file = request.files["pdf-file"]
    form_type = request.form.get("form-type")

    if form_type not in FORM_FIELDS:
        return jsonify({"error": "Invalid form type selected"}), 400

    pdf_path = os.path.join("uploads", pdf_file.filename)
    pdf_file.save(pdf_path)

    extracted_text = extract_text_from_pdf(pdf_path)
    expected_fields = FORM_FIELDS[form_type]

    missing_fields = find_missing_fields(extracted_text, expected_fields)

    os.remove(pdf_path)

    if not missing_fields:
        result = {"message": "The form is correctly formatted. No missing fields!"}
    else:
        result = {"missing_fields": missing_fields}

    return jsonify(result)

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(host="127.0.0.3", port=5000, debug=True)
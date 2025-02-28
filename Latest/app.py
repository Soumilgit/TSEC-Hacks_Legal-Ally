import os
import re
import docx
import gradio as gr
from pymongo import MongoClient

# MongoDB Connection Setup
client = MongoClient(MONGO_URI)  
db = client["LegalCasesDB"]
collection = db["Cases"]

# IPC to BNS Mapping with Implications
law_mapping = {
    r"IPC Section 124A": {"new_law": "BNS Section 150", "implication": "Redefined to include acts endangering sovereignty, unity, and integrity of India, with stricter penalties."},
    r"IPC Section 302": {"new_law": "BNS Section 101", "implication": "Punishment remains the same—death or life imprisonment with a fine."},
    r"IPC Section 304": {"new_law": "BNS Section 103", "implication": "Procedural changes introduced for trial and investigation."},
    r"IPC Section 307": {"new_law": "BNS Section 106", "implication": "Attempt to murder now linked to actual harm caused for sentencing."},
    r"IPC Section 326": {"new_law": "BNS Section 127", "implication": "Includes acid attacks and legal framework for victim compensation."},
    r"IPC Section 354": {"new_law": "BNS Section 74", "implication": "Stricter laws for sexual harassment and harassment in public spaces."},
    r"IPC Section 376": {"new_law": "BNS Section 63", "implication": "Stricter punishments, including harsher penalties for gang rape and repeat offenders."},
    r"IPC Section 392": {"new_law": "BNS Section 303", "implication": "Stronger provisions for violent robbery."},
    r"IPC Section 395": {"new_law": "BNS Section 305", "implication": "Includes provisions for armed robbery and organized crime syndicates."},
    r"IPC Section 467": {"new_law": "BNS Section 328", "implication": "Forgery laws expanded to include digital fraud and cyber crimes."},
    r"IPC Section 420": {"new_law": "BNS Section 246", "implication": "Cheating and fraud penalties increased for large-scale financial crimes."},
    r"IPC Section 506": {"new_law": "BNS Section 356", "implication": "Includes online threats and intimidation."},
    r"IPC Section 509": {"new_law": "BNS Section 72", "implication": "Includes verbal, non-verbal, and online harassment of women."},
    r"IPC Section 120B": {"new_law": "BNS Section 61", "implication": "Conspiracy laws updated to target organized crime more effectively."},
}

# Function to Extract Text from Word Document
def extract_text_from_docx(file_path):
    """Extracts text from a Word (.docx) document."""
    try:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        return f"Error reading document: {e}"

# Function to Replace IPC Sections with BNS Sections and Store Implications
def convert_ipc_to_bns(text):
    """Replaces IPC sections with corresponding BNS sections while storing implications."""
    updated_text = text
    replaced_laws = []

    sentences = text.split(". ")
    modified_sentences = []

    for sentence in sentences:
        modified_sentence = sentence
        for ipc_section, details in law_mapping.items():
            if re.search(ipc_section, sentence, re.IGNORECASE):
                modified_sentence = re.sub(ipc_section, details["new_law"], modified_sentence, flags=re.IGNORECASE)
                replaced_laws.append(f"{ipc_section} → {details['new_law']} | {details['implication']}")
        modified_sentences.append(modified_sentence)

    updated_text = ". ".join(modified_sentences)

    return updated_text, replaced_laws

# Generate Unique Case ID
def generate_case_id():
    """Generates a unique case ID based on existing records."""
    last_case = collection.find_one({}, sort=[("case_id", -1)])  
    if last_case and "case_id" in last_case:
        last_id = int(last_case["case_id"].split("_")[-1])
        new_id = f"BNS_2025_{last_id + 1:03d}"
    else:
        new_id = "BNS_2025_001"
    return new_id

# Function to Process File Upload
# Function to Process File Upload
def process_uploaded_file(file):
    """Processes uploaded DOCX file and converts IPC laws to BNS laws."""
    file_path = file.name  # Get temporary file path
    ipc_text = extract_text_from_docx(file_path)

    if not ipc_text:
        return "Could not extract text from document.", "", ""

    bns_text, replaced_laws = convert_ipc_to_bns(ipc_text)

    case_id = generate_case_id()

    # Store in MongoDB
    bns_case = {
        "case_id": case_id,
        "original_text": ipc_text,
        "updated_text": bns_text,
        "replaced_laws": replaced_laws
    }

    message = "✅ Case successfully stored."  # Default success message

    try:
        collection.insert_one(bns_case)
    except Exception as e:
        message = f"❌ Error storing case in MongoDB: {e}"

    return message, bns_text, "\n".join(replaced_laws)

custom_css = """
body {
    background-color: #ffffff; /* White Background */
    color: #003366; /* Dark Blue Text */
}
h1, h2, h3 {
    color: #004080; /* Header Text - Dark Blue */
}
button {
    background-color: #007BFF !important; /* Blue Buttons */
    color: white !important;
    border-radius: 8px;
}
button:hover {
    background-color: #0056b3 !important; /* Darker Blue on Hover */
}
textarea, input {
    border: 1px solid #004080 !important; /* Blue Borders */
    background-color: #f0f8ff !important; /* Light Blue Input Background */
    color: #003366 !important; /* Dark Blue Text */
}
"""

# Modify Gradio Interface with Custom Styling
iface = gr.Interface(
    fn=process_uploaded_file,
    inputs=gr.File(type="filepath"),
    outputs=[
        gr.Textbox(label="Processing Result"),
        gr.Textbox(label="Updated BNS Case", lines=10),
        gr.Textbox(label="Old Laws Replaced with New Laws & Their Implications", lines=10)
    ],
    title="Old to New Document Converter",
    css=custom_css  # Apply Custom Blue-White Theme
)

# Run Gradio App
iface.launch()
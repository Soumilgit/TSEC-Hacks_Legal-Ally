import streamlit as st
import PyPDF2
import docx
from transformers import pipeline

# Load AI Model (Legal-BERT)
legal_ner = pipeline("ner", model="nlpaueb/legal-bert-base-uncased", aggregation_strategy="simple")
legal_text_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    text = ""
    reader = PyPDF2.PdfReader(uploaded_file)
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# Function to extract text from DOCX
def extract_text_from_docx(uploaded_file):
    doc = docx.Document(uploaded_file)
    return "\n".join([para.text for para in doc.paragraphs])

# High-risk clause categories
risk_categories = [
    "termination without cause",
    "non-compete clause",
    "data privacy violations",
    "liquidated damages",
    "intellectual property disputes",
    "confidentiality breaches",
]

# Function to detect high-risk clauses using AI
def detect_risk_clauses(contract_text):
    results = legal_text_classifier(contract_text, risk_categories, multi_label=True)
    high_risk_clauses = []

    for label, score in zip(results["labels"], results["scores"]):
        if score > 0.4:  # Adjust threshold as needed
            high_risk_clauses.append((label, score))
    
    return high_risk_clauses

# Safer alternative suggestions
suggestions = {
    "termination without cause": "Consider requiring prior notice and valid justification.",
    "non-compete clause": "Limit non-compete clauses to a reasonable time and geographic scope.",
    "data privacy violations": "Ensure compliance with GDPR by defining data retention policies.",
    "liquidated damages": "Damages should be limited to actual proven losses.",
    "intellectual property disputes": "Clearly define IP ownership and licensing terms.",
    "confidentiality breaches": "Include clear confidentiality obligations with time limits."
}

# Function to suggest safer alternatives
def suggest_alternatives(risk_found):
    return {clause: suggestions.get(clause, "No suggestion available.") for clause, _ in risk_found}

# Streamlit UI
st.title("AI-Powered Contract Review")

uploaded_file = st.file_uploader("Upload Contract (PDF/DOCX)", type=["pdf", "docx"])

if uploaded_file:
    # Extract text
    if uploaded_file.name.endswith(".pdf"):
        contract_text = extract_text_from_pdf(uploaded_file)
    else:
        contract_text = extract_text_from_docx(uploaded_file)
    
    st.subheader("Extracted Contract Text:")
    st.text_area("Contract Content", contract_text, height=200)

    # Detect high-risk clauses using AI
    high_risk_found = detect_risk_clauses(contract_text)
    
    if high_risk_found:
        st.subheader("⚠️ High-Risk Clauses Identified:")
        for clause, score in high_risk_found:
            st.write(f"- *{clause}* (Risk Score: {score:.2f})")

        # Suggest safer alternatives
        safer_alternatives = suggest_alternatives(high_risk_found)
        st.subheader("✅ Suggested Safer Alternatives:")
        for clause, alternative in safer_alternatives.items():
            st.write(f"- *{clause}* → {alternative}")
    else:
        st.success("No high-risk clauses detected.")
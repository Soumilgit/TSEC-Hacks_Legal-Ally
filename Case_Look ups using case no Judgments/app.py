import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Load CSV with all columns as strings to avoid NaN issues
df = pd.read_csv("judgments.csv", dtype=str).fillna("N/A")  # Replace NaN with "N/A"

def search_case(case_number):
    # Ensure 'case_no' is a string before searching
    df['case_no'] = df['case_no'].astype(str)
    
    # Search for case number
    result = df[df['case_no'].str.contains(case_number, na=False, case=False)]
    
    if result.empty:
        return None
    else:
        details = result.iloc[0].to_dict()  # Get first match
        return {
            "case_no": details.get('case_no', 'N/A'),
            "pet": details.get('pet', 'N/A'),
            "res": details.get('res', 'N/A'),
            "pet_adv": details.get('pet_adv', 'N/A'),
            "res_adv": details.get('res_adv', 'N/A'),
            "bench": details.get('bench', 'N/A'),
            "judgement_by": details.get('judgement_by', 'N/A'),
            "judgment_date": details.get('judgment_dates', 'N/A'),
            "pdf_link": f"https://api.sci.gov.in/{details.get('temp_link', '')}"
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    case_number = request.form.get('case_number', '').strip()
    result = search_case(case_number)
    
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "No details found for this case."})

if __name__ == "__main__":
     app.run(host="127.0.0.4", port=5000, debug=True)

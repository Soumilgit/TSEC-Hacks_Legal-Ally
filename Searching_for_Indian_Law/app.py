from flask import Flask, render_template, request, jsonify
import pandas as pd
import google.generativeai as genai

# Define the API key directly
GOOGLE_API_KEY = ""

if not GOOGLE_API_KEY:
    raise ValueError("Error: GOOGLE_API_KEY is not set. Please add your API key directly.")

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Load the dataset
file_path = "indian_laws_and_acts_v2.csv"
df = pd.read_csv(file_path)
df['published_date'] = pd.to_datetime(df['published_date'], errors='coerce')
df['commencement_date'] = pd.to_datetime(df['commencement_date'], errors='coerce')

app = Flask(__name__)

# Function to search laws
def search_laws(keyword, sort_by, order, limit):
    results = df[df['title'].str.contains(keyword, case=False, na=False)]
    if results.empty:
        return []

    results = results.dropna(subset=[sort_by])
    results = results.sort_values(by=sort_by, ascending=(order == "asc"))
    
    return results[['title', 'url', sort_by]].head(limit).to_dict(orient='records')

# Function to summarize laws
def summarize_law(title):
    prompt = f"Summarize the law titled '{title}' in 2-3 sentences."
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text.strip() if response and hasattr(response, 'text') else "Summary not available."
    except Exception as e:
        return f"Error: {str(e)}"

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# API Route for searching laws
@app.route('/search', methods=['POST'])
def search():
    data = request.json
    keyword = data.get('keyword', '').strip()
    sort_by = "published_date" if data.get('sort_by') == "P" else "commencement_date"
    order = "asc" if data.get('order', 'desc') == "asc" else "desc"
    limit = int(data.get('limit', 10))

    laws = search_laws(keyword, sort_by, order, limit)

    return jsonify(laws)

# API Route for summarizing laws
@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    title = data.get('title', '')

    summary = summarize_law(title)
    return jsonify({"summary": summary})

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify, send_file
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

# Import Services
from services.serper import find_official_website, search_company_info
from services.crawler import crawl_website
from services.openrouter import analyze_company
from services.pdf_generator import generate_pdf
from services.discord import send_to_discord

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')
os.makedirs('tmp', exist_ok=True)

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/research', methods=['POST'])
def research():
    data = request.json
    company_input = data.get('companyInput')
    ai_model = data.get('aiModel', 'openai/gpt-4o-mini')

    if not company_input:
        return jsonify({'error': 'Company name or URL is required'}), 400

    website_url = company_input
    
    # 1. Check if input is a URL or name
    if not is_valid_url(company_input):
        # Use Serper to find the website
        print(f"Finding official website for: {company_input}")
        found_url = find_official_website(company_input)
        if found_url:
            website_url = found_url
        else:
            # Continue without website crawling if not found
            pass

    # 2. Crawl website
    scraped_text = ""
    if is_valid_url(website_url):
        print(f"Crawling website: {website_url}")
        scraped_text = crawl_website(website_url)

    # 3. Use Serper to find extra info if scraping failed or is too small
    if len(scraped_text) < 500:
        print("Scraping returned little data. Falling back to Serper search for summary.")
        extra_info = search_company_info(company_input)
        if extra_info and 'organic' in extra_info:
            for item in extra_info['organic'][:3]:
                scraped_text += f"\nTitle: {item.get('title')}\nSnippet: {item.get('snippet')}\n"

    # 4. OpenRouter AI Analysis
    print(f"Analyzing data using model: {ai_model}")
    report_data = analyze_company(scraped_text, company_input, model=ai_model)
    
    # Override website if we found it and AI didn't catch it
    if not report_data.get('website') and is_valid_url(website_url):
        report_data['website'] = website_url

    return jsonify(report_data)

@app.route('/api/pdf', methods=['POST'])
def create_pdf():
    data = request.json
    try:
        filepath = generate_pdf(data)
        # Store filepath in app context or session if needed, but for now just return URL
        # We can serve it via a GET route
        filename = os.path.basename(filepath)
        return jsonify({'success': True, 'pdfUrl': f'/api/download/{filename}'})
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/download/<filename>', methods=['GET'])
def download_pdf(filename):
    filepath = os.path.join('tmp', filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return "File not found", 404

@app.route('/api/discord', methods=['POST'])
def send_discord():
    data = request.json
    report_data = data.get('reportData')
    pdf_url = data.get('pdfUrl', '')
    settings = data.get('settings', {})
    
    if pdf_url.startswith('/api/download/'):
        filename = pdf_url.replace('/api/download/', '')
        pdf_filepath = os.path.join('tmp', filename)
    else:
        pdf_filepath = ''

    success, message = send_to_discord(report_data, pdf_filepath, settings)
    
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': message}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

import os
import requests
import json

def get_openrouter_api_key():
    return os.getenv('OPENROUTER_API_KEY')

def analyze_company(text_content, company_name_or_url, model='openai/gpt-4o-mini'):
    """Sends the scraped text to OpenRouter to extract company details."""
    api_key = get_openrouter_api_key()
    if not api_key or api_key == "YOUR_OPENROUTER_API_KEY_HERE":
        print("Warning: OpenRouter API key not set.")
        return {
            'companyName': company_name_or_url,
            'website': '',
            'phoneNumber': '',
            'address': '',
            'productsServices': 'OpenRouter API Key not set. Cannot perform AI analysis.',
            'painPoints': '',
            'competitors': []
        }

    url = "https://openrouter.ai/api/v1/chat/completions"
    
    prompt = f"""
    Analyze the following extracted text from a company's website (or related to {company_name_or_url}).
    Please extract or infer the following information and return it strictly as a JSON object:
    - companyName: The official name of the company.
    - website: The official website URL (if found in text).
    - phoneNumber: The official contact phone number (if found).
    - address: The physical address or headquarters (if found).
    - productsServices: A brief paragraph describing their main products or services.
    - painPoints: A brief paragraph describing the potential pain points or problems their products/services solve for their customers.
    - competitors: An array of objects, each containing 'name' (competitor company name) and 'website' (competitor website URL). Suggest up to 3 competitors operating in the same industry.

    Extracted Text:
    {text_content[:15000]}
    
    Return ONLY valid JSON.
    """

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful business research AI. Always return strict, valid JSON with no markdown wrapping or extra text."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        content = result['choices'][0]['message']['content']
        return json.loads(content)
    except Exception as e:
        print(f"OpenRouter API error: {e}")
        return {
            'companyName': company_name_or_url,
            'website': '',
            'phoneNumber': '',
            'address': '',
            'productsServices': f'Error performing AI analysis: {e}',
            'painPoints': '',
            'competitors': []
        }

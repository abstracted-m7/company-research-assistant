import os
import requests
import json
from urllib.parse import urlparse

def get_serper_api_key():
    return os.getenv('SERPER_API_KEY')

def search_company_info(query):
    """Searches Serper.dev for company info."""
    api_key = get_serper_api_key()
    if not api_key or api_key == "YOUR_SERPER_API_KEY_HERE":
        print("Warning: Serper API key not set.")
        return None

    url = "https://google.serper.dev/search"
    payload = json.dumps({
        "q": query,
        "num": 5
    })
    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Serper API error: {e}")
        return None

def find_official_website(company_name):
    """Finds the official website URL using Serper.dev."""
    result = search_company_info(f"{company_name} official website")
    if not result or 'organic' not in result or len(result['organic']) == 0:
        return None
    
    # Try to find a reasonable top result
    for res in result['organic']:
        link = res.get('link', '')
        if link and 'wikipedia.org' not in link and 'linkedin.com' not in link and 'bloomberg.com' not in link:
            # Basic validation
            try:
                parsed = urlparse(link)
                return f"{parsed.scheme}://{parsed.netloc}"
            except:
                pass
    return result['organic'][0].get('link')

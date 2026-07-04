import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_text_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        script.decompose()
        
    text = soup.get_text(separator=' ', strip=True)
    # clean up extra whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def extract_internal_links(soup, base_url):
    links = set()
    for a in soup.find_all('a', href=True):
        href = a['href']
        # Ignore anchor links or javascript
        if href.startswith('#') or href.startswith('javascript:'):
            continue
            
        full_url = urljoin(base_url, href)
        # Ensure it's internal
        if urlparse(full_url).netloc == urlparse(base_url).netloc:
            links.add(full_url)
    return list(links)

def crawl_website(url, max_pages=3):
    """Crawls a website and returns extracted text from main pages."""
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to crawl {url}: {e}")
        return ""
        
    soup = BeautifulSoup(response.text, 'html.parser')
    text_content = get_text_from_html(response.text)
    
    if max_pages > 1:
        links = extract_internal_links(soup, url)
        # Prioritize about, products, services, contact
        priority_keywords = ['about', 'product', 'service', 'solution', 'contact']
        priority_links = [l for l in links if any(k in l.lower() for k in priority_keywords)]
        
        pages_to_crawl = priority_links[:max_pages - 1]
        
        for link in pages_to_crawl:
            try:
                res = requests.get(link, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
                if res.status_code == 200:
                    text_content += "\n\n--- Page: " + link + " ---\n"
                    text_content += get_text_from_html(res.text)
            except:
                pass
                
    # Limit text to avoid blowing up LLM context (e.g. 15000 characters)
    return text_content[:15000]

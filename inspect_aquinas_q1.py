import requests
from bs4 import BeautifulSoup
import sys

def inspect(url):
    print(f"--- Inspecting {url} ---")
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.encoding = 'latin-1'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check text content size
        text = soup.get_text()
        print(f"Text length: {len(text)}")
        print(f"Snippet: {text[:200]}")
        
        # Check for sub-links
        count = 0
        for link in soup.find_all('a'):
            href = link.get('href')
            text_link = link.get_text(strip=True)
            if href and count < 10:
                 print(f"Link: {text_link}, Href: {href}")
                 count += 1
    except Exception as e:
        print(f"Error: {e}")

inspect("https://www.thelatinlibrary.com/aquinas/q1.1.shtml")

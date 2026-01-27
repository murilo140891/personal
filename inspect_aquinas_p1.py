import requests
from bs4 import BeautifulSoup
import sys

def inspect(url):
    print(f"--- Inspecting {url} ---")
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.encoding = 'latin-1'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for link in soup.find_all('a'):
            href = link.get('href')
            text = link.get_text(strip=True)
            if href:
                 print(f"Text: {text}, Href: {href}")
    except Exception as e:
        print(f"Error: {e}")

inspect("https://www.thelatinlibrary.com/aquinas/p1.shtml")

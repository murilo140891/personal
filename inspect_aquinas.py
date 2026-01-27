import requests
from bs4 import BeautifulSoup
import sys

url = "https://www.thelatinlibrary.com/aquinas.html"
try:
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    response.encoding = 'latin-1' # Common for older sites, or utf-8
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    print(f"Links found on {url}:")
    for link in soup.find_all('a'):
        href = link.get('href')
        text = link.get_text(strip=True)
        if href and 'aquinas' in href:
            print(f"Text: {text}, Href: {href}")

except Exception as e:
    print(f"Error: {e}")

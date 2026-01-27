import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import re
import subprocess

BASE_URL = "https://isidore.co/aquinas/summa/"
START_URL = "https://isidore.co/aquinas/summa/index.html"
ROOT_DIR = "suma-teologica-latim"

# Mapping prefix to readable name for folders
PREFIX_MAP = {
    "FP": "1-Prima-Pars",
    "FS": "2-Prima-Secundae",
    "SS": "3-Secunda-Secundae",
    "TP": "4-Tertia-Pars",
    "XP": "5-Supplementum",
    "X1": "6-Appendix-I",
    "X2": "7-Appendix-II"
}

visited = set()

def get_soup(url):
    try:
        # Respectful delay
        time.sleep(0.5)
        # Use curl to bypass python ssl issues
        result = subprocess.run(
            ["curl", "-s", "-L", "-k", "--http1.1", url], 
            capture_output=True, 
            text=True, 
            encoding='utf-8', 
            errors='ignore'
        )
        if result.returncode != 0:
            print(f"Error fetching {url}: Return code {result.returncode}")
            return None
            
        return BeautifulSoup(result.stdout, 'html.parser')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def is_latin(text):
    text_lower = text.lower()
    
    english_words = ["the", "of", "to", "and", "is", "that", "it", "for", "by", "with", "whether", "objection", "reply", "answer", "on", "contrary", "we", "have", "no", "need", "any", "further", "knowledge", "man", "seek", "know", "what", "above", "reason"]
    latin_words = ["et", "in", "ad", "non", "ut", "sed", "est", "quod", "de", "cum", "per", "respondeo", "dicendum", "praeterea", "videtur", "ergo", "prima", "pars", "quaestio", "articulus", "prooemium", "summa", "theologia", "sacra", "doctrina", "scientia", "deus", "res", "argumentum", "fides", "ratio"]
    
    english_score = 0
    latin_score = 0
    
    tokens = re.findall(r'\b[a-z]+\b', text_lower)
    token_set = set(tokens)
    
    for word in english_words:
        if word in token_set:
            english_score += 1
            
    for word in latin_words:
        if word in token_set:
            latin_score += 1
            
    if english_score > 0 and latin_score == 0:
        return False
    if latin_score > 0 and english_score == 0:
        return True
    
    if english_score == 0 and latin_score == 0:
        # Fallback for very short text?
        # Assume False unless we are sure
        return False
        
    return latin_score >= english_score

def extract_latin_content(soup):
    latin_blocks = []
    seen_blocks = set()
    
    # Identify tables that likely contain content
    # Use cellpadding="12" as primary identifier
    tables = soup.find_all('table', attrs={"cellpadding": "12"})
    if not tables:
         tables = soup.find_all('table') # Fallback
    
    for table in tables:
        rows = table.find_all('tr')
        if not rows:
            continue
            
        for row in rows:
            cols = row.find_all('td')
            text_to_add = None
            
            # Case 1: Standard bilingual row (Latin | English)
            if len(cols) >= 2:
                raw_text = cols[0].get_text(separator="\n").strip()
                if raw_text and is_latin(raw_text):
                     text_to_add = raw_text
                
            # Case 2: Single column header/content
            elif len(cols) == 1:
                raw_text = cols[0].get_text(separator="\n").strip()
                result = is_latin(raw_text)
                if len(raw_text) > 3 and result:
                     # STRICT FILTER
                     if not any(nav in raw_text.lower() for nav in ["index", "first part", "second part", "question:", "article:", "next", "previous", "prologue", "treatise"]):
                        text_to_add = raw_text
            
            if text_to_add:
                # Normalize for deduplication
                normalized = re.sub(r'\s+', '', text_to_add)
                if normalized not in seen_blocks:
                    latin_blocks.append(text_to_add)
                    seen_blocks.add(normalized)

    return "\n\n".join(latin_blocks)

def get_target_info(url):
    parsed = urlparse(url)
    rel_path = parsed.path.replace("/aquinas/summa/", "").lstrip("/")
    
    if not rel_path or rel_path == "index.html":
        return None, None # Skip index.html for saving Latin content
    
    parts = rel_path.split("/")
    
    if len(parts) == 1:
        # This is likely a part index (e.g., FP.html)
        return None, None
    
    # This is a content page (e.g., FP/FP001.html)
    prefix = parts[0]
    folder = PREFIX_MAP.get(prefix, prefix)
    filename = parts[-1].replace(".html", ".md")
    
    target_dir = os.path.join(ROOT_DIR, folder)
    target_path = os.path.join(target_dir, filename)
    
    return target_dir, target_path

def crawl(url):
    if url in visited:
        return
    visited.add(url)
    
    print(f"Crawling: {url}")
    soup = get_soup(url)
    if not soup:
        return
    
    # 1. Extraction
    target_dir, target_path = get_target_info(url)
    if target_path:
        latin_text = extract_latin_content(soup)
        if latin_text:
            os.makedirs(target_dir, exist_ok=True)
            with open(target_path, "w", encoding="utf-8") as f:
                title = soup.title.string if soup.title else os.path.basename(target_path)
                f.write(f"# {title}\n\n")
                f.write(latin_text)
            print(f"  Saved to: {target_path}")

    # 2. Recursion
    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        if not href or href.startswith("#") or "http" in href and "isidore.co" not in href:
            continue
            
        full_url = urljoin(url, href)
        full_url = full_url.split("#")[0]
        
        # Only stay within the Summa directory
        if full_url.startswith(BASE_URL) and full_url.endswith(".html"):
            crawl(full_url)

def main():
    os.makedirs(ROOT_DIR, exist_ok=True)
    crawl(START_URL)

if __name__ == "__main__":
    main()

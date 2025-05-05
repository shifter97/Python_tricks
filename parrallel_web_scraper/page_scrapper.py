import requests
from bs4 import BeautifulSoup
import threading
import logging
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

class FileReaderCM:
    def __init__(self, filepath, mode='r', **kwargs):
        self.filepath = filepath
        self.mode = mode
        self.kwargs = kwargs

    def __enter__(self):
        self.file = open(self.filepath, self.mode, **self.kwargs)
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()


class JsonListWriter:
    def __init__(self, filepath, **kwargs):
        self.filepath = filepath
        self.kwargs = kwargs
        self.data = []

    def __enter__(self):
        return self

    def write(self, obj):
        self.data.append(obj)

    def __exit__(self, exc_type, exc_value, traceback):
        with open(self.filepath, 'w', encoding='utf-8', **self.kwargs) as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)


URLS_FILE = 'parrallel_web_scraper/urls.txt'
OUTPUT_FILE = 'parrallel_web_scraper/results.json'
LOG_FILE = 'parrallel_web_scraper/scraper.log'
MAX_WORKERS = 5

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(threadName)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, mode='a'),
        logging.StreamHandler()
    ]
)

lock = threading.Lock()
results = []


def fetch_and_parse(url):
    try:
        logging.info(f"Starting fetch: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        title_tag = soup.find('title')
        p_tag = soup.find('p')

        title = title_tag.get_text(strip=True) if title_tag else None
        first_paragraph = p_tag.get_text(strip=True) if p_tag else None

        logging.info(f"Fetched: {url}")
        return {'url': url, 'title': title, 'first_paragraph': first_paragraph}

    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")
        return {'url': url, 'error': str(e)}


with FileReaderCM(URLS_FILE) as f:
    urls = [line.strip() for line in f if line.strip()]
logging.info(f"Loaded {len(urls)} URLs from {URLS_FILE}")


with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    future_to_url = {executor.submit(fetch_and_parse, url): url for url in urls}
    for future in as_completed(future_to_url):
        data = future.result()
        with lock:
            results.append(data)

    
with JsonListWriter(OUTPUT_FILE) as writer:
    for item in results:
            writer.write(item)
logging.info(f"Saved results to {OUTPUT_FILE}")


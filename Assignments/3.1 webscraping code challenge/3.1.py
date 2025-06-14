import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib.error

def news_scraper():
    url = 'https://www.nation.africa'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    
    print(f'Scraping latest news from: {url}\n')
    print('Attempt 1: Using requests library')
    
    try:     #first try with requests
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        print('Succefully fetched content using request')
        return extract_news(soup)
    
    except requests.exceptions.RequestException as req_err:
        print(f'Requests failed: {req_err}')
        print('\nAttempt 2: Using urllib Library')
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as response:
                html = response.read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            print('Successfully fetched content using urllib')
            return extract_news(soup)
        
        except urllib.error.URLError as url_err:
            print(f'urllib failed: {url_err}')
            print('\nAll scraping attempts failed. Please check your internet connections and try again later')
            
            return None
        
def extract_news(soup):         #find all news atricle containers
    articles = soup.find_all('div', class_='story-teaser')
    
    if not articles:
        print('No articles found. Website structure might have changed. ')
        return None
    
    news_items = []
    print('\nExtracted News Articles:\n' + '=' * 60)
    
    for article in articles:        #Extract headline
        headline_elem = article.find('h3', class_='tease-title')
        headline = headline_elem.get_text(strip=True) if headline_elem else 'No headline available'
        
        summary_elem = article.find('p', class_='teaser-summary')
        summary = summary_elem.get_text(strip=True) if summary_elem else 'No summary available'
        
        news_items.append((headline, summary))
        print(f'. {headline}')
        print(f'  {summary}')
        print('-' * 60)
        
    print(f'\nTotal articles extracted: {len(news_items)}')
    return news_items


if __name__=='__main__':
    news_scraper()
        
    
            
    
    
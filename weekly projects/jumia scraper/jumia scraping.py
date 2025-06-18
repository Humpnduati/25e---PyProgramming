import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import re
from datetime import datetime

# Configure settings
MAX_PAGES = 5
BASE_URL = "https://www.jumia.co.ke/smartphones/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
DELAY = 1.5  # Seconds between requests
CSV_FILENAME = f"jumia_products_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"

def scrape_page(url):
    """Scrape product data from a single page URL"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_product_data(product):
    """Extract product details from a product card"""
    try:
        name_tag = product.find('h3', class_='name')
        name = name_tag.text.strip() if name_tag else 'N/A'
        
        price_tag = product.find('div', class_='prc')
        price = price_tag.text.strip() if price_tag else 'N/A'
        
        # Handle discount percentage
        discount_tag = product.find('div', class_='bdg _dsct')
        discount = discount_tag.text.strip() if discount_tag else '0%'
        
        # Handle ratings
        rating_tag = product.find('div', class_='stars _s')
        rating = rating_tag.text.strip() if rating_tag else 'N/A'
        
        # Extract numeric rating from style attribute
        rating_style = rating_tag.get('style', '') if rating_tag else ''
        rating_width = re.search(r'width: (\d+)%', rating_style)
        numeric_rating = float(rating_width.group(1))/20 if rating_width else 0.0
        
        review_tag = product.find('div', class_='rev')
        reviews = review_tag.text.strip() if review_tag else '0'
        
        # Extract numeric review count
        review_count = int(re.search(r'(\d+)', reviews).group(1)) if reviews != '0' else 0
        
        # Extract product URL and image
        link = product.find('a', class_='core')['href']
        full_url = f"https://www.jumia.co.ke{link}"
        img_tag = product.find('img', class_='img')
        img_url = img_tag['data-src'] if img_tag and 'data-src' in img_tag.attrs else img_tag['src'] if img_tag else 'N/A'

        return {
            'name': name,
            'price': price,
            'discount': discount,
            'rating_text': rating,
            'numeric_rating': round(numeric_rating, 1),
            'review_count': review_count,
            'product_url': full_url,
            'image_url': img_url
        }
    except Exception as e:
        print(f"Error extracting product data: {e}")
        return None

def main():
    products = []
    
    with open(CSV_FILENAME, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'name', 'price', 'discount', 'rating_text', 
            'numeric_rating', 'review_count', 'product_url', 'image_url'
        ])
        writer.writeheader()
        
        for page in range(1, MAX_PAGES + 1):
            page_url = f"{BASE_URL}?page={page}"
            print(f"Scraping page {page}: {page_url}")
            
            soup = scrape_page(page_url)
            if not soup:
                continue
                
            product_cards = soup.find_all('article', class_='prd')
            
            if not product_cards:
                print(f"No products found on page {page}. Stopping.")
                break
                
            for card in product_cards:
                product_data = extract_product_data(card)
                if product_data:
                    writer.writerow(product_data)
                    products.append(product_data)
            
            time.sleep(DELAY + random.uniform(0, 1))  # Randomized delay
            
    print(f"\nSuccessfully scraped {len(products)} products")
    print(f"Data saved to {CSV_FILENAME}")

if __name__ == "__main__":
    main()
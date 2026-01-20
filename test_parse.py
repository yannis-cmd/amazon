#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'fr-FR,fr;q=0.9'
}
url = 'https://www.amazon.fr/s?k=souris&page=1'

print('Fetching Amazon...')
response = requests.get(url, headers=headers, timeout=20)
print(f'Status: {response.status_code}')

soup = BeautifulSoup(response.content, 'html.parser')
items = soup.find_all('div', {'data-component-type': 's-search-result'})
print(f'Total items found: {len(items)}')

articles = []
for i, item in enumerate(items[:20]):
    try:
        # Title
        title = 'N/A'
        title_elem = item.find('h2')
        if title_elem:
            span = title_elem.find('span')
            if span:
                title = span.text.strip()
        
        # Price
        price = 'N/A'
        price_elem = item.find('span', {'class': 'a-price-whole'})
        if price_elem:
            price = price_elem.text.strip()
        
        print(f"{i+1}. {title[:40]:40} | {price}")
        
        if title != 'N/A' and price != 'N/A':
            articles.append({'titre': title, 'prix': price})
        
    except Exception as e:
        print(f"  Error parsing item {i}: {e}")

print(f'\nTotal articles extracted: {len(articles)}')

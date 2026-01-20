#!/usr/bin/env python3
"""
🔍 Test de recherche Amazon - Debug
Affiche ce qui est retourné par Amazon.fr
"""

import requests
from bs4 import BeautifulSoup
import json

def test_amazon_search(query="iPhone 15"):
    """Test la recherche Amazon"""
    print(f"\n🔍 Teste: {query}\n")
    
    url = f"https://www.amazon.fr/s?k={query.replace(' ', '+')}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'fr-FR,fr;q=0.9',
    }
    
    try:
        print(f"📡 URL: {url}\n")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Taille: {len(response.content)} bytes\n")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # TOUS les sélecteurs possibles
        print("=" * 70)
        print("🔎 CHERCHANT LES ARTICLES...")
        print("=" * 70)
        
        # 1. Chercher par data-component-type
        print("\n1️⃣ Cherchant: div[data-component-type='s-search-result']")
        items = soup.find_all('div', {'data-component-type': 's-search-result'})
        print(f"   ✅ Trouvé: {len(items)} items\n")
        
        # 2. Chercher par data-component-type='s-result-item'
        print("2️⃣ Cherchant: div[data-component-type='s-result-item']")
        items2 = soup.find_all('div', {'data-component-type': 's-result-item'})
        print(f"   ✅ Trouvé: {len(items2)} items\n")
        
        # 3. Chercher par classe
        print("3️⃣ Cherchant: div[class*='s-result-item']")
        items3 = soup.find_all('div', {'class': lambda x: x and 's-result-item' in x if x else False})
        print(f"   ✅ Trouvé: {len(items3)} items\n")
        
        # 4. Chercher tous les h2 (titres)
        print("4️⃣ Cherchant: tous les h2")
        all_h2 = soup.find_all('h2')
        print(f"   ✅ Trouvé: {len(all_h2)} h2\n")
        
        # Utiliser le meilleur
        items = items if len(items) > 0 else items2
        items = items if len(items) > 0 else items3
        
        print(f"\n✅ Sélecteur final: {len(items)} articles trouvés\n")
        
        articles = []
        for i, item in enumerate(items[:5]):  # Premier 5
            print(f"\n{'─' * 70}")
            print(f"📦 ARTICLE {i+1}")
            print(f"{'─' * 70}")
            
            # Titre
            title = "N/A"
            title_elem = item.find('h2')
            if title_elem:
                span = title_elem.find('span')
                if span:
                    title = span.text.strip()
                else:
                    title = title_elem.text.strip()
            
            print(f"📝 Titre: {title[:60]}...")
            
            # Prix
            price = "N/A"
            price_elem = item.find('span', {'class': 'a-price-whole'})
            if price_elem:
                price = price_elem.text.strip()
            else:
                # Alternative
                price_elem = item.find('span', {'class': lambda x: x and 'a-price' in x if x else False})
                if price_elem:
                    price = price_elem.text.strip()
            
            print(f"💰 Prix: {price}")
            
            # URL
            url_item = "N/A"
            link = item.find('a')
            if link and 'href' in link.attrs:
                url_item = link['href']
            
            print(f"🔗 URL: {url_item[:60]}...")
            
            # Image
            img = "N/A"
            img_elem = item.find('img')
            if img_elem and 'src' in img_elem.attrs:
                img = img_elem['src'][:60] + "..."
            
            print(f"🖼️  Image: {img}")
            
            articles.append({
                'titre': title,
                'prix': price,
                'url': url_item,
                'image': img
            })
        
        print(f"\n{'=' * 70}")
        print(f"✅ RÉSULTAT FINAL: {len(articles)} articles")
        print(f"{'=' * 70}\n")
        
        print(json.dumps(articles, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_amazon_search("iPhone 15")

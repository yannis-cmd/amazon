#!/usr/bin/env python3
"""
🔍 Test spécifique "clavier gamer" - Debug détaillé
"""

import requests
from bs4 import BeautifulSoup
import json

def test_clavier_gamer():
    """Test la recherche Amazon pour clavier gamer"""
    query = "clavier gamer"
    print(f"\n🔍 TEST: {query}\n")
    
    url = f"https://www.amazon.fr/s?k={query.replace(' ', '+')}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'fr-FR,fr;q=0.9',
    }
    
    try:
        print(f"📡 URL: {url}\n")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Taille: {len(response.content)} bytes\n")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Chercher les items
        print("🔎 CHERCHANT LES ARTICLES...\n")
        
        items = soup.find_all('div', {'data-component-type': 's-search-result'})
        print(f"✅ Trouvé: {len(items)} div[data-component-type='s-search-result']\n")
        
        if len(items) == 0:
            print("❌ Aucun item trouvé avec s-search-result!")
            print("\n🔎 Essayant d'autres sélecteurs...\n")
            
            # Essayer d'autres sélecteurs
            items2 = soup.find_all('div', {'data-component-type': 's-result-item'})
            print(f"  s-result-item: {len(items2)}")
            
            items3 = soup.find_all('div', {'class': lambda x: x and 's-result-item' in str(x)})
            print(f"  class contenant 's-result-item': {len(items3)}")
            
            all_divs = soup.find_all('div', {'data-component-type': True})
            print(f"  Tous les div avec data-component-type: {len(all_divs)}")
            
            if all_divs:
                print(f"\n  Types trouvés:")
                types = set()
                for d in all_divs[:20]:
                    dt = d.get('data-component-type', 'unknown')
                    types.add(dt)
                for t in types:
                    print(f"    - {t}")
            
            return
        
        print(f"{'─' * 70}\n")
        
        articles = []
        for i, item in enumerate(items[:10]):
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
            
            print(f"📝 Titre: {title[:70]}...")
            
            # Prix
            price = "N/A"
            price_elem = item.find('span', {'class': 'a-price-whole'})
            if price_elem:
                price = price_elem.text.strip()
            else:
                # Chercher dans tous les spans avec 'a-price'
                spans = item.find_all('span')
                for s in spans:
                    cls = s.get('class', [])
                    if isinstance(cls, list):
                        cls_str = ' '.join(cls)
                    else:
                        cls_str = str(cls)
                    
                    if 'a-price' in cls_str:
                        text = s.text.strip()
                        if any(c.isdigit() for c in text):
                            price = text
                            break
            
            print(f"💰 Prix: {price}")
            
            # Image
            img = "N/A"
            img_elem = item.find('img')
            if img_elem and 'src' in img_elem.attrs:
                img = "✅ Trouvée"
            
            print(f"🖼️  Image: {img}")
            
            print()
            
            articles.append({
                'titre': title,
                'prix': price,
            })
        
        print(f"✅ RÉSULTAT: {len(articles)} articles extraits\n")
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_clavier_gamer()

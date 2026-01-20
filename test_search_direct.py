#!/usr/bin/env python3
"""Test simple search"""
import sys
sys.path.insert(0, 'C:\\Users\\eisbr\\Nouveau dossier')

from app_web_v2_1 import search_amazon_all

print("\nTesting search directly...")
results = search_amazon_all("souris", page=1)
print(f"\nRESULTS: {len(results)} articles")
if results:
    print(f"First: {results[0]}")

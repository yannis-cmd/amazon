"""
Test Script - Vérifie que l'application démarre correctement
"""

import sys
import os

print("[TEST] Starting Amazon Tracker Pro verification...")
print(f"[TEST] Python version: {sys.version}")
print(f"[TEST] Working directory: {os.getcwd()}")

# Test 1: Imports
print("\n[TEST 1] Testing imports...")
try:
    import config
    import constants
    import utils
    import logger
    import exceptions
    import validators
    print("[PASS] All modules imported successfully")
except Exception as e:
    print(f"[FAIL] Import error: {e}")
    sys.exit(1)

# Test 2: Configuration
print("\n[TEST 2] Testing configuration...")
try:
    from config import ui_config, data_config, amazon_config
    assert ui_config.WINDOW_WIDTH == 1200
    assert data_config.MAX_RESULTS == 10
    print("[PASS] Configuration loaded correctly")
except Exception as e:
    print(f"[FAIL] Configuration error: {e}")
    sys.exit(1)

# Test 3: Logger
print("\n[TEST 3] Testing logger...")
try:
    from logger import logger
    logger.info("Test message - Logger working!")
    print("[PASS] Logger initialized successfully")
except Exception as e:
    print(f"[FAIL] Logger error: {e}")
    sys.exit(1)

# Test 4: Validators
print("\n[TEST 4] Testing validators...")
try:
    from validators import (
        validate_search_query,
        validate_price,
        validate_budget
    )
    
    assert validate_search_query("souris gamer") == True
    assert validate_search_query("") == False
    assert validate_price(29.99) == True
    assert validate_price(-10) == False
    assert validate_budget(20, 50) == True
    
    print("[PASS] Validators working correctly")
except Exception as e:
    print(f"[FAIL] Validator error: {e}")
    sys.exit(1)

# Test 5: Utils
print("\n[TEST 5] Testing utils...")
try:
    from utils import format_price, extract_budget_from_text
    
    formatted = format_price(29.99)
    assert formatted is not None
    
    budget = extract_budget_from_text("Je veux une souris pour 50 euros")
    # May be None if pattern not matched, but shouldn't error
    
    print("[PASS] Utils working correctly")
except Exception as e:
    print(f"[FAIL] Utils error: {e}")
    sys.exit(1)

# Test 6: Data files
print("\n[TEST 6] Checking data files...")
try:
    import json
    from pathlib import Path
    
    # Check if BD file exists
    db_file = Path("articles_tracked.json")
    if db_file.exists():
        with open(db_file) as f:
            data = json.load(f)
        print(f"[PASS] Database file exists ({len(data)} items)")
    else:
        print("[PASS] Database file will be created on first use")
    
except Exception as e:
    print(f"[FAIL] Data file error: {e}")
    sys.exit(1)

# Test 7: Try loading tkinter
print("\n[TEST 7] Testing tkinter...")
try:
    import tkinter as tk
    print("[PASS] tkinter available")
except Exception as e:
    print(f"[FAIL] tkinter not available: {e}")
    print("      (tkinter is required for GUI)")
    sys.exit(1)

print("\n" + "="*60)
print("[SUCCESS] All startup tests PASSED!")
print("="*60)
print("\nYou can now run: python main.py")
print("Or directly: python amazon_tracker.py")

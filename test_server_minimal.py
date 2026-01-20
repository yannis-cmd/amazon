#!/usr/bin/env python3
"""Minimal test to isolate the issue"""
import sys
import os
import signal

print("=" * 50)
print("Python version:", sys.version)
print("Working dir:", os.getcwd())
print("=" * 50)

# Test 1: Import app_web_v2_1
print("\n[TEST 1] Importing app_web_v2_1...")
try:
    from app_web_v2_1 import app
    print("[OK] App imported successfully")
except Exception as e:
    print(f"[FAIL] Failed to import app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Check routes
print("\n[TEST 2] Checking routes...")
routes = [str(rule) for rule in app.url_map.iter_rules()]
logs_routes = [r for r in routes if 'logs' in r]
print(f"  Found {len(logs_routes)} routes with 'logs':")
for r in logs_routes:
    print(f"    - {r}")

# Test 3: Import waitress
print("\n[TEST 3] Importing waitress...")
try:
    from waitress import serve
    print("[OK] Waitress imported")
except Exception as e:
    print(f"[FAIL] {e}")
    sys.exit(1)

# Test 4: Start server
print("\n[TEST 4] Starting Waitress on port 3000...")
print("  Waiting for requests. Make requests in another terminal.")
print("=" * 50)

def signal_handler(sig, frame):
    print("\n[SIGNAL] Shutdown requested")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

try:
    print("[SERVE] About to call serve()...")
    sys.stdout.flush()
    sys.stderr.flush()
    
    # Wrap serve in try-except to catch hidden exceptions
    try:
        serve(app, host='0.0.0.0', port=3000, _quiet=False)
    except KeyboardInterrupt:
        print("\n[SERVE-INNER] KeyboardInterrupt")
    except SystemExit:
        print("\n[SERVE-INNER] SystemExit")
        raise
    except Exception as e:
        print(f"\n[SERVE-INNER] Exception in serve(): {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("[SERVE] serve() returned normally")
except KeyboardInterrupt:
    print("\n[SERVE] KeyboardInterrupt at top level")
except Exception as e:
    print(f"\n[SERVE] Exception at top level: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    print("[SERVE] Finally block executed")


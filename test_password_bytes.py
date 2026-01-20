password_bytes = b"tg"
print(f"Password: {password_bytes.decode()}")
print(f"Length: {len(password_bytes.decode())}")
print(f"Hex: {password_bytes.hex()}")
print(f"Ord values: {[ord(c) for c in password_bytes.decode()]}")

# Check if it matches 't' and 'g'
test = "tg"
print(f"\nTest match with 'tg': {password_bytes.decode() == test}")
print(f"Test match with 'tg' lower: {password_bytes.decode().lower() == test.lower()}")

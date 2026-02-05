#!/usr/bin/env python3
"""
Test script to diagnose bcrypt issues
"""

import sys
import traceback

print("Testing bcrypt installation...")

try:
    import bcrypt
    print(f"[OK] bcrypt imported successfully. Version: {getattr(bcrypt, '__version__', 'unknown')}")
except ImportError as e:
    print(f"[ERROR] Failed to import bcrypt: {e}")
    sys.exit(1)

try:
    import passlib
    print(f"[OK] passlib imported successfully. Version: {getattr(passlib, '__version__', 'unknown')}")
except ImportError as e:
    print(f"[ERROR] Failed to import passlib: {e}")
    sys.exit(1)

try:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    print("[OK] Created CryptContext successfully")

    # Test with a short password
    password = "shortpass"
    print(f"Attempting to hash password: '{password}' (length: {len(password)})")

    hashed = pwd_context.hash(password)
    print(f"[OK] Successfully hashed password: {hashed[:30]}...")

except Exception as e:
    print(f"[ERROR] Error during hashing: {e}")
    traceback.print_exc()

    # Try alternative approach - maybe we need to specify the backend
    try:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__ident="2b")
        hashed = pwd_context.hash(password)
        print(f"[OK] Alternative approach worked: {hashed[:30]}...")
    except Exception as e2:
        print(f"[ERROR] Alternative approach also failed: {e2}")
        traceback.print_exc()

print("\nTesting verification...")
try:
    # Test verification
    test_password = "shortpass"
    test_hash = pwd_context.hash(test_password)
    is_valid = pwd_context.verify(test_password, test_hash)
    print(f"[OK] Verification works: {is_valid}")
except Exception as e:
    print(f"[ERROR] Verification failed: {e}")
    traceback.print_exc()
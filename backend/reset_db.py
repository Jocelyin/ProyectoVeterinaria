import os
import time

DB_FILE = "veterinaria.db"

def reset_db():
    if os.path.exists(DB_FILE):
        try:
            os.remove(DB_FILE)
            print(f"[OK] Deleted {DB_FILE}")
        except Exception as e:
            print(f"[FAIL] Could not delete {DB_FILE}: {e}")
    else:
        print(f"[OK] {DB_FILE} does not exist.")

if __name__ == "__main__":
    reset_db()

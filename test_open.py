import os
import sys

os.add_dll_directory(r"D:\brlcad\build\bin")
os.add_dll_directory(r"D:\python-brlcad")
sys.path.insert(0, r"D:\python-brlcad")

from _brlcad import ffi, lib

db_path = r"D:/brlcad/build/bin/random_csg.g"

count = lib.brlcad_open_db(db_path.encode())
print(f"✅ Opened: {db_path}")
print(f"📦 Objects in database: {count}")

print("\n📋 Object list:")
lib.brlcad_list_objects(db_path.encode())

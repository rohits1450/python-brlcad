import os, sys
os.add_dll_directory(r"D:\brlcad\build\bin")
sys.path.insert(0, r"D:\python-brlcad")

from _brlcad import ffi, lib

db = r"D:/brlcad/build/bin/random_csg.g"
objects = ["prim_0.s", "prim_1.s", "random_csg.c", "nonexistent"]

print(f"📦 Objects in DB: {lib.brlcad_open_db(db.encode())}")

print("\n📋 All objects:")
lib.brlcad_list_objects(db.encode())

print("\n🔍 Object types:")
for obj in objects:
    t = ffi.string(lib.brlcad_get_object_type(db.encode(), obj.encode())).decode()
    print(f"  {obj:20s} → {t}")

print("\n✅ Existence check:")
for obj in objects:
    exists = lib.brlcad_object_exists(db.encode(), obj.encode())
    print(f"  {obj:20s} → {'exists' if exists else 'NOT FOUND'}")

print("\n📐 Bounding box (random_csg.c):")
min_pt = ffi.new("double[3]")
max_pt = ffi.new("double[3]")
ret = lib.brlcad_get_bounding_box(db.encode(), b"random_csg.c", min_pt, max_pt)
if ret == 0:
    print(f"  min: ({min_pt[0]:.2f}, {min_pt[1]:.2f}, {min_pt[2]:.2f})")
    print(f"  max: ({max_pt[0]:.2f}, {max_pt[1]:.2f}, {max_pt[2]:.2f})")
else:
    print("  ❌ bbox failed")

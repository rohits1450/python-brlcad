import sys
sys.path.insert(0, r"D:\python-brlcad")

import brlcad

# Open database
db = brlcad.open(r"D:/brlcad/build/bin/random_csg.g")
print(db)

# Object count
print(f"\n Total objects: {db.object_count()}")

# Query individual objects
for name in ["prim_0.s", "prim_1.s", "random_csg.c", "nonexistent"]:
    if db.exists(name):
        obj = db.get(name)
        print(f"\n🔷 {obj}")
        print(f"   type  : {obj.type}")
        bbox = obj.bounding_box
        if bbox:
            print(f"   bbox  : {bbox}")
            print(f"   center: {bbox.center}")
            print(f"   size  : {bbox.size}")
    else:
        print(f"\n '{name}' not found")

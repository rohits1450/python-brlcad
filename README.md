# BRL-CAD PYTHON BINDINGS

A Python binding prototype for [BRL-CAD](https://brlcad.org/) using CFFI, exposing
BRL-CAD's core geometry database (`librt`) to Python.

Built as part of a GSoC 2026 proposal for the
**Python Geometry Bindings** project under BRL-CAD by Rohit S

---

## What It Does

- Opens a BRL-CAD `.g` geometry database from Python
- Lists all objects in the database
- Queries object types (`solid`, `combination`, `region`)
- Checks object existence by name
- Computes 3D bounding boxes via `librt` raytracer

---

## Architecture

- `test_open.py` → Python entry point
- `_brlcad.pyd` → CFFI compiled extension
- `brlcad_wrap.c` → C wrapper over BRL-CAD librt
- BRL-CAD `librt` / `libbu` → core geometry engine
- `.g` file → geometry database


---

## Requirements

- BRL-CAD compiled from source (tested with BRL-CAD trunk, Windows)
- Python 3.13+
- CFFI (`pip install cffi`)

---

## Build

```powershell
cd D:\python-brlcad
python build_brlcad.py
This compiles brlcad_wrap.c into _brlcad.cp313-win_amd64.pyd.
```
## Usage
```
python
import os, sys
os.add_dll_directory(r"D:\brlcad\build\bin")
sys.path.insert(0, r"D:\python-brlcad")

from _brlcad import ffi, lib

db = r"D:/brlcad/build/bin/random_csg.g"

# Count objects
print(lib.brlcad_open_db(db.encode()))          # → 7

# List all objects
lib.brlcad_list_objects(db.encode())

# Get object type
t = ffi.string(lib.brlcad_get_object_type(db.encode(), b"prim_0.s")).decode()
print(t)                                         # → "solid"

# Check existence
lib.brlcad_object_exists(db.encode(), b"prim_0.s")   # → 1

# Bounding box
min_pt = ffi.new("double")
max_pt = ffi.new("double")
lib.brlcad_get_bounding_box(db.encode(), b"random_csg.c", min_pt, max_pt)
print(f"min: ({min_pt:.2f}, {min_pt:.2f}, {min_pt:.2f})")
print(f"max: ({max_pt:.2f}, {max_pt:.2f}, {max_pt:.2f})")
```
## Sample Output
```
 Objects in DB: 7

📋 All objects:
_GLOBAL, prim_0.s, prim_1.s, prim_2.s, prim_3.s, prim_4.s, random_csg.c

🔍 Object types:
  prim_0.s             → solid
  prim_1.s             → solid
  random_csg.c         → combination
  nonexistent          → not_found

📐 Bounding box (random_csg.c):
  min: (-39.00, -20.00, -16.00)
  max: (18.00, 15.00, 35.00)
```  
## Files
| File            | Purpose                      |
| --------------- | ---------------------------- |
| brlcad_wrap.c   | C wrapper over BRL-CAD librt |
| brlcad_wrap.h   | Public C API header          |
| build_brlcad.py | CFFI build script            |
| test_open.py    | Python demo and test         |
| random_csg.c    | Generates sample .g database |



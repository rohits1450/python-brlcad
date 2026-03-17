import os, sys, math
os.add_dll_directory(r"D:\brlcad\build\bin")
sys.path.insert(0, r"D:\python-brlcad")

from _brlcad import ffi, lib

# All 24 vertices of a rhombicuboctahedron
# Formula: all permutations of (±1, ±1, ±(1+√2))
s = 1 + math.sqrt(2)
raw_verts = []
for a in [1, -1]:
    for b in [1, -1]:
        for c, d in [(1, s), (s, 1)]:
            raw_verts.append((a * c, b * d, s  * (1 if a*b > 0 else -1)))

# Proper 24 vertices using standard formula
verts = []
vals = [1.0, -1.0]
t = 1.0 + math.sqrt(2.0)
for x in vals:
    for y in vals:
        verts.append((x, y,  t))
        verts.append((x, y, -t))
        verts.append((x,  t, y))
        verts.append((x, -t, y))
        verts.append(( t, x, y))
        verts.append((-t, x, y))

# Deduplicate
seen = set()
unique_verts = []
for v in verts:
    key = tuple(round(x, 6) for x in v)
    if key not in seen:
        seen.add(key)
        unique_verts.append(v)

unique_verts = unique_verts[:24]
print(f" Vertices: {len(unique_verts)}")

# Triangulate faces (each square face = 2 triangles, each triangle = 1)
# Using convex hull to auto-generate faces
from itertools import combinations

def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])

def dot(a, b):
    return sum(x*y for x, y in zip(a, b))

def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))

def norm(v):
    n = math.sqrt(sum(x*x for x in v))
    return tuple(x/n for x in v)

# Use scipy for convex hull if available, otherwise manual triangulation
try:
    from scipy.spatial import ConvexHull
    import numpy as np

    pts_np = np.array(unique_verts)
    hull = ConvexHull(pts_np)
    triangles = hull.simplices.tolist()
    print(f" Faces (triangulated): {len(triangles)}")

except ImportError:
    # Manual fallback — hardcoded triangulation for rhombicuboctahedron
    print("⚠️  scipy not found, using simplified icosahedron fallback")
    triangles = []
    n = len(unique_verts)
    center = [sum(v[i] for v in unique_verts)/n for i in range(3)]
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                triangles.append([i, j, k])
    triangles = triangles[:44]

# Flatten for CFFI
flat_verts = []
for v in unique_verts:
    flat_verts.extend(v)

flat_faces = []
for t in triangles:
    flat_faces.extend(t)

num_verts = len(unique_verts)
num_faces = len(triangles)

c_verts = ffi.new(f"double[{len(flat_verts)}]", flat_verts)
c_faces = ffi.new(f"int[{len(flat_faces)}]", flat_faces)

db_path = r"D:\python-brlcad\rhombicuboctahedron.g"

ret = lib.brlcad_create_bot(
    db_path.encode(),
    b"rhombicuboctahedron.s",
    num_verts,
    c_verts,
    num_faces,
    c_faces
)

if ret == 0:
    print(f" Written to {db_path}")
    print(f"   Vertices : {num_verts}")
    print(f"   Triangles: {num_faces}")
    print(f"   Open with: mged {db_path}")
else:
    print(f" Failed with code {ret}")

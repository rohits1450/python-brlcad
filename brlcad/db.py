import os
import sys

os.add_dll_directory(r"D:\brlcad\build\bin")
sys.path.insert(0, r"D:\python-brlcad")

from _brlcad import ffi, lib


class BoundingBox:
    def __init__(self, min_pt, max_pt):
        self.min = tuple(min_pt[i] for i in range(3))
        self.max = tuple(max_pt[i] for i in range(3))

    @property
    def center(self):
        return tuple((self.min[i] + self.max[i]) / 2 for i in range(3))

    @property
    def size(self):
        return tuple(self.max[i] - self.min[i] for i in range(3))

    def __repr__(self):
        return f"BoundingBox(min={self.min}, max={self.max})"


class GeometryObject:
    def __init__(self, db, name):
        self._db = db
        self.name = name

    @property
    def type(self):
        t = lib.brlcad_get_object_type(
            self._db._path.encode(), self.name.encode()
        )
        return ffi.string(t).decode()

    @property
    def bounding_box(self):
        min_pt = ffi.new("double[3]")
        max_pt = ffi.new("double[3]")
        ret = lib.brlcad_get_bounding_box(
            self._db._path.encode(), self.name.encode(), min_pt, max_pt
        )
        if ret != 0:
            return None
        return BoundingBox(min_pt, max_pt)

    @property
    def exists(self):
        return bool(lib.brlcad_object_exists(
            self._db._path.encode(), self.name.encode()
        ))

    def __repr__(self):
        return f"GeometryObject(name='{self.name}', type='{self.type}')"


class Database:
    def __init__(self, path):
        self._path = path
        count = lib.brlcad_open_db(path.encode())
        if count < 0:
            raise FileNotFoundError(f"Cannot open BRL-CAD database: {path}")
        self._count = count

    def list_objects(self):
        results = []
        # capture stdout trick via names we already know
        # use direct listing call
        lib.brlcad_list_objects(self._path.encode())

    def object_count(self):
        return self._count

    def get(self, name):
        obj = GeometryObject(self, name)
        if not obj.exists:
            raise KeyError(f"Object '{name}' not found in database")
        return obj

    def exists(self, name):
        return bool(lib.brlcad_object_exists(
            self._path.encode(), name.encode()
        ))

    def get_type(self, name):
        t = lib.brlcad_get_object_type(
            self._path.encode(), name.encode()
        )
        return ffi.string(t).decode()

    def bounding_box(self, name):
        return self.get(name).bounding_box

    def __repr__(self):
        return f"Database(path='{self._path}', objects={self._count})"

import cffi
import os

ffi = cffi.FFI()

ffi.cdef("""
    int brlcad_open_db(const char *filename);
    void brlcad_list_objects(const char *filename);
""")

BRLCAD_BUILD = r"D:/brlcad/build"
BRLCAD_SRC   = r"D:/brlcad"

ffi.set_source(
    "_brlcad",
    open("brlcad_wrap.c").read(),
    libraries=["librt", "libbu", "libwdb"],
    library_dirs=[
        os.path.join(BRLCAD_BUILD, "lib"),
        os.path.join(BRLCAD_BUILD, "bin"),
    ],
    include_dirs=[
        os.path.join(BRLCAD_BUILD, "include"),
        os.path.join(BRLCAD_SRC, "include"),
    ],
)

if __name__ == "__main__":
    ffi.compile(verbose=True)
    print("Build successful!")

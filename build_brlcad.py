import cffi
import os

ffi = cffi.FFI()

ffi.cdef("""
    int         brlcad_open_db(const char *filename);
    void        brlcad_list_objects(const char *filename);
    const char* brlcad_get_object_type(const char *filename, const char *objname);
    int         brlcad_get_bounding_box(const char *filename, const char *objname,
                                        double *min_pt, double *max_pt);
    int         brlcad_object_exists(const char *filename, const char *objname);
         int brlcad_create_bot(const char *filename, const char *objname,
                      int num_vertices, double *vertices,
                      int num_faces, int *faces);

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

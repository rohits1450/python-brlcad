#include "bu/app.h"
#include "rt/db_io.h"
#include "rt/db_internal.h"
#include "raytrace.h"
#include "brlcad_wrap.h"
#include "wdb.h"

int brlcad_open_db(const char *filename) {
    struct db_i *dbip;
    dbip = db_open(filename, DB_OPEN_READONLY);
    if (dbip == DBI_NULL) return -1;
    if (db_dirbuild(dbip) < 0) {
        db_close(dbip);
        return -1;
    }
    int count = (int)dbip->dbi_nrec;
    db_close(dbip);
    return count;
}

void brlcad_list_objects(const char *filename) {
    struct db_i *dbip;
    struct directory *dp;
    int i;
    dbip = db_open(filename, DB_OPEN_READONLY);
    if (dbip == DBI_NULL) return;
    db_dirbuild(dbip);
    for (i = 0; i < RT_DBNHASH; i++) {
        for (dp = dbip->dbi_Head[i]; dp != RT_DIR_NULL; dp = dp->d_forw) {
            printf("%s\n", dp->d_namep);
        }
    }
    db_close(dbip);
}

const char* brlcad_get_object_type(const char *filename, const char *objname) {
    struct db_i *dbip;
    struct directory *dp;
    const char *type;

    dbip = db_open(filename, DB_OPEN_READONLY);
    if (dbip == DBI_NULL) return "error";
    db_dirbuild(dbip);

    dp = db_lookup(dbip, objname, LOOKUP_QUIET);
    if (dp == RT_DIR_NULL) {
        db_close(dbip);
        return "not_found";
    }

    if (dp->d_flags & RT_DIR_COMB) {
        if (dp->d_flags & RT_DIR_REGION)
            type = "region";
        else
            type = "combination";
    } else if (dp->d_flags & RT_DIR_SOLID) {
        type = "solid";
    } else {
        type = "unknown";
    }

    db_close(dbip);
    return type;
}

int brlcad_get_bounding_box(const char *filename, const char *objname,
                              double *min_pt, double *max_pt) {
    struct rt_i *rtip;
    rtip = rt_dirbuild(filename, NULL, 0);
    if (rtip == RTI_NULL) return -1;

    if (rt_gettree(rtip, objname) < 0) {
        rt_free_rti(rtip);
        return -1;
    }

    rt_prep_parallel(rtip, 1);

    min_pt[0] = rtip->mdl_min[X];
    min_pt[1] = rtip->mdl_min[Y];
    min_pt[2] = rtip->mdl_min[Z];
    max_pt[0] = rtip->mdl_max[X];
    max_pt[1] = rtip->mdl_max[Y];
    max_pt[2] = rtip->mdl_max[Z];

    rt_free_rti(rtip);
    return 0;
}

int brlcad_object_exists(const char *filename, const char *objname) {
    struct db_i *dbip;
    struct directory *dp;
    dbip = db_open(filename, DB_OPEN_READONLY);
    if (dbip == DBI_NULL) return 0;
    db_dirbuild(dbip);
    dp = db_lookup(dbip, objname, LOOKUP_QUIET);
    db_close(dbip);
    return (dp != RT_DIR_NULL) ? 1 : 0;
}

int brlcad_create_bot(const char *filename, const char *objname,
                      int num_vertices, double *vertices,
                      int num_faces, int *faces) {
    struct rt_wdb *wdbp;
    wdbp = wdb_fopen(filename);
    if (wdbp == NULL) return -1;

    /* Convert flat double array to point_t array */
    point_t *pts = (point_t *)bu_malloc(num_vertices * sizeof(point_t), "pts");
    for (int i = 0; i < num_vertices; i++) {
        pts[i][X] = vertices[i * 3 + 0];
        pts[i][Y] = vertices[i * 3 + 1];
        pts[i][Z] = vertices[i * 3 + 2];
    }

    /* Convert flat int array to face indices */
    int *face_arr = (int *)bu_malloc(num_faces * 3 * sizeof(int), "faces");
    for (int i = 0; i < num_faces * 3; i++) {
        face_arr[i] = faces[i];
    }

    int ret = mk_bot(wdbp, objname, RT_BOT_SOLID, RT_BOT_UNORIENTED, 0,
                     num_vertices, num_faces,
                     pts, face_arr, NULL, 0);

    bu_free(pts, "pts");
    bu_free(face_arr, "faces");
    wdb_close(wdbp);
    return ret;
}

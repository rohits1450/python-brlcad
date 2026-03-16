#include "bu/app.h"
#include "rt/db_io.h"
#include "rt/db_internal.h"
#include "raytrace.h"

/* Opens a .g file, returns number of objects. -1 on error */
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

/* List object names — prints to stdout */
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

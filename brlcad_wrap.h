#ifndef BRLCAD_WRAP_H
#define BRLCAD_WRAP_H

#ifdef __cplusplus
extern "C" {
#endif

/* Opens .g file, returns object count. -1 on error */
int brlcad_open_db(const char *filename);

/* Prints all object names to stdout */
void brlcad_list_objects(const char *filename);

/* Returns type string: "solid", "combination", "region", "unknown", "not_found" */
const char* brlcad_get_object_type(const char *filename, const char *objname);

/* Fills min[3] and max[3] with bounding box. Returns 0 on success, -1 on error */
int brlcad_get_bounding_box(const char *filename, const char *objname,
                             double *min_pt, double *max_pt);

/* Returns 1 if object exists, 0 if not */
int brlcad_object_exists(const char *filename, const char *objname);

#ifdef __cplusplus
}
#endif

#endif /* BRLCAD_WRAP_H */

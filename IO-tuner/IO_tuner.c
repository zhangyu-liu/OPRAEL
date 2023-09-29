#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdio.h>
#include <string.h>
#include "mpi.h"

// Function pointer typedef for the real MPI_File_open
typedef int (*MPI_File_open_t)(MPI_Comm, const char *, int, MPI_Info, MPI_File *);

// Replace original MPI_File_open function with custom implementation
int MPI_File_open(MPI_Comm comm, const char *filename, int amode, MPI_Info info, MPI_File *fh) {
    int (*real_MPI_File_open)(MPI_Comm, const char *, int, MPI_Info, MPI_File *);
    real_MPI_File_open = (MPI_File_open_t)dlsym(RTLD_NEXT, "MPI_File_open");

    char striping_factor[4];
    char striping_unit[15];
    char romio_cb_read_s[10];
    char romio_cb_write_s[10];
    char romio_ds_read_s[10];
    char romio_ds_write_s[10];
    int romio_cb_read;
    int romio_cb_write;
    int romio_ds_read;
    int romio_ds_write;
    char cb_nodes[4];
    int cb_config_list;
    char cb_config_list_s[4]="*:";
    char cb_s[3];
    FILE *fp;

    fp = fopen("/path/hint.txt","r");

    fscanf(fp,"%s", striping_factor);
    fscanf(fp,"%s", striping_unit);
    fscanf(fp,"%d", &romio_cb_read);
    fscanf(fp,"%d", &romio_cb_write);
    fscanf(fp,"%d", &romio_ds_read);
    fscanf(fp,"%d", &romio_ds_write);
    fscanf(fp,"%s", cb_nodes);
    fscanf(fp,"%d", &cb_config_list);
    if(romio_cb_read == 0)
        strcpy(romio_cb_read_s,"automatic");
    else if (romio_cb_read == 1)
        strcpy(romio_cb_read_s,"disable");
    else if (romio_cb_read == 2)
        strcpy(romio_cb_read_s,"enable");
    if(romio_cb_write == 0)
        strcpy(romio_cb_write_s,"automatic");
    else if (romio_cb_write == 1)
        strcpy(romio_cb_write_s,"disable");
    else if (romio_cb_write == 2)
        strcpy(romio_cb_write_s,"enable");
    if(romio_ds_read == 0)
        strcpy(romio_ds_read_s,"automatic");
    else if (romio_ds_read == 1)
        strcpy(romio_ds_read_s,"disable");
    else if (romio_ds_read == 2)
        strcpy(romio_ds_read_s,"enable");
    if(romio_ds_write == 0)
        strcpy(romio_ds_write_s,"automatic");
    else if (romio_ds_write == 1)
        strcpy(romio_ds_write_s,"disable");
    else if (romio_ds_write == 2)
        strcpy(romio_ds_write_s,"enable");
    sprintf(cb_s,"%d",cb_config_list);
    strcat(cb_config_list_s,cb_s);


    // Modify the info object to set stripe information
    MPI_Info_set(info, "striping_factor",striping_factor); 
    MPI_Info_set(info, "striping_unit", striping_unit);
    MPI_Info_set(info, "romio_cb_read", romio_cb_read_s); 
    MPI_Info_set(info, "romio_cb_write",romio_cb_write_s); 
    MPI_Info_set(info, "romio_ds_read", romio_ds_read_s); 
    MPI_Info_set(info, "romio_ds_write", romio_ds_write_s); 
    MPI_Info_set(info, "cb_nodes", cb_nodes); 
    MPI_Info_set(info, "cb_config_list", cb_config_list_s); 
    
    fclose(fp);

    return real_MPI_File_open(comm, filename, amode, info, fh);
}


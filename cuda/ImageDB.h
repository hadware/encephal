#ifndef IMAGEDB_H
#define IMAGEDB_H

#include <stdlib.h>

typedef struct labeled_image {
  unsigned char label;
  float * img;
} LImage;

typedef struct image_database {
  int number;
  size_t image_size;
  LImage * db;
} ImageDB;

#endif
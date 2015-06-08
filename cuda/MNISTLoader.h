#ifndef MNISTLOADER_H
#define MNISTLOADER_H

#include "ImageDB.h"

extern ImageDB * readMNIST_db(int number_image, const char * filename);
extern void printImage(const LImage * img, size_t size);
extern void addMNISTLabel(ImageDB * db, const char * filename);

#endif
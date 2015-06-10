#ifndef MNISTLOADER_H
#define MNISTLOADER_H

#include "ImageDB.h"

/*
* Read a MNIST database from the file and return the number_image from the file into
* a ImageDB.
*/
extern ImageDB * readMNIST_db(int number_image, const char * filename);

/*
* Print the image to stdout.
*/
extern void printImage(const LImage * img, size_t size);

/*
* Add the label to the ImageDB from the label file.
*/
extern void addMNISTLabel(ImageDB * db, const char * filename);

#endif
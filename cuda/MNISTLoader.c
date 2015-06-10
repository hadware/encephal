#include <stdlib.h>
#include <math.h>
#include <stdio.h>
#include <assert.h>

#include "MNISTLoader.h"


static int reverseInt(int i) {
	return ((i & 255) << 24) |
		(((i >> 8) & 255) << 16) |
		(((i >> 16) & 255) << 8) |
		((i >> 24) & 255);
}

ImageDB * readMNIST_db(int number_image, const char * filename) {

printf("%s\n", filename);
    FILE * file = fopen(filename, "rb");

	if (file == NULL) {
		perror("Impossible d'ouvrir le fichier");
		exit(-1);
	}

	ImageDB * db = (ImageDB*)malloc(sizeof(ImageDB));
	assert(db);

	int magic = 0;
	fread(&magic, sizeof(int), 1, file);

	int number_img_read = 0;
	fread(&number_img_read, sizeof(int), 1, file);
	number_img_read = reverseInt(number_img_read);

	int width = 0;
	int height = 0;

	fread(&height, sizeof(int), 1, file);
	height = reverseInt(height);

	fread(&width, sizeof(int), 1, file);
	width = reverseInt(width);

	int number = (number_image > number_img_read ? number_img_read : number_image);

	db->number = number;
	db->image_size = height * width * sizeof(float);
	db->db = (LImage*)malloc(sizeof(LImage) * number);
	assert(db->db);

	unsigned char temp = 0;
	for (int i = 0; i < number; i++) {
		db->db[i].img = (float*)malloc(db->image_size);
		assert(db->db[i].img);

		for (int l = 0; l < height; l++) {
			for (int c = 0; c < width; c++) {
				fread(&temp, sizeof(char), 1, file);
				db->db[i].img[width * l + c] = ((float)temp / (float)255);
			}
		}
	}
	fclose(file);

	return db;
}

void addMNISTLabel(ImageDB * db, const char * filename) {
	FILE * file = fopen(filename, "rb");
	assert(file);

	int number_img = 0;
	fread(&number_img, sizeof(int), 1, file); /* magic number */

	fread(&number_img, sizeof(int), 1, file); /* number image */
	number_img = reverseInt(number_img);
	assert(number_img >= db->number);

	for (int i = 0; i < db->number; i++) {
		fread(&(db->db[i].label), sizeof(unsigned char), 1, file);
		assert(db->db[i].label < 10);
	}

	fclose(file);
}

void printImage(const LImage * img, size_t size) {
	//square
	int dim = size / sizeof(float);
	int side = (int)sqrt(dim);
	assert(side * side == dim);

	printf("%d\n", img->label);
	for (int l = 0; l < side; l++) {
		for (int c = 0; c < side; c++)
			(img->img[l * side + c] > 0.5 ? printf("#") : printf(" "));
		printf("\n");
	}
}

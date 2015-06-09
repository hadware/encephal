#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <limits.h>
#include "CudaNetwork.h"
//extern "C" {
	#include "MNISTLoader.h"
//}

DTYPE * encoder(DTYPE * buffer, size_t taille, int value) {
	memset(buffer, 0, taille);
	buffer[value] = 1;
	return buffer;
}

int decoder(DTYPE * buffer, int size) {
	int res = 0;
	DTYPE value = buffer[0];
	for (int i = 1; i < size; i++) {
		if (buffer[i] > value) {
			value = buffer[i];
			res = i;
		}
	}
	return res;
}

void dirname(char * path) {
	int index = 0;
	int last = -1;
	while (path[index]) {
		if (path[index] == '\\')
			last = index;
		index++;
	}
	if (last != -1)
		path[last] = '\0';
}

int main(int argc, char *argv[]) {

	NNetworkDescriptor descriptor;

	descriptor.nodes.push_back(FCONNECTION);
	descriptor.nodes.push_back(PERCEPTRON);
	descriptor.nodes.push_back(FCONNECTION);
	descriptor.nodes.push_back(PERCEPTRON);
/*
	descriptor.connection.push_back(1);
	descriptor.connection.push_back(2);
	descriptor.connection.push_back(3);
	descriptor.connection.push_back(4);
*/	
	descriptor.buffer_size.push_back(784);
	descriptor.buffer_size.push_back(200);
	descriptor.buffer_size.push_back(200);
	descriptor.buffer_size.push_back(10);
	descriptor.buffer_size.push_back(10);

	CudaNetwork network;
	network.loadNetwork(descriptor);
	uint32_t size_out = network.getOutputSize();

	DTYPE * buffer_out = (DTYPE*)malloc(sizeof(DTYPE) * size_out);
	
	DTYPE * buffer_learning = (DTYPE*)malloc(sizeof(DTYPE) * size_out);

	ImageDB * db_learn = readMNIST_db(60000, "../MNIST/train-images-idx3-ubyte");
	addMNISTLabel(db_learn, "../MNIST/train-labels-idx1-ubyte");
	clock_t start = clock(), diff;

	encoder(buffer_learning, sizeof(DTYPE) * size_out, db_learn->db[0].label);
	
	printf("---------- Apprentissage ----------\n");
	
	const uint32_t MAXSTAR = 80;
	int step = db_learn->number / MAXSTAR;
	
	for (int i = 0; i < 80; i++)
		printf("*");

	printf("\n");

	for (int32_t i = 0; i < db_learn->number; i++) {
		network.setInput(db_learn->db[i].img);
		network.learning(buffer_learning, 0.5);

		if (i % step == 0) {
			printf("*");
			fflush(stdout);
		}

		if (i < db_learn->number)
			encoder(buffer_learning, sizeof(DTYPE) * size_out, db_learn->db[i + 1].label);
		
		network.wait_finish();

	}
	printf("\n");

	diff = clock() - start;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	printf("learning : %d seconds %d milliseconds\n", msec / 1000, msec % 1000);

	printf("---------- Test --------- \n");

	ImageDB * db_test = readMNIST_db(1000, "../MNIST/t10k-images-idx3-ubyte");
	addMNISTLabel(db_test, "../MNIST/t10k-labels-idx1-ubyte");

	int accum = 0;
	for (int32_t i = 0; i < db_test->number; i++) {
		network.setInput(db_test->db[i].img);
		network.propagation();
		network.wait_finish();
		network.getOutput(buffer_out);

		if (decoder(buffer_out, 10) == db_test->db[i].label)
			accum++;
	}

	printf("%f\n", ((float)accum) / db_test->number);
	getc(stdin);

	return 0;
}


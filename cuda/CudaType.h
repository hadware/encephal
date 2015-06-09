#ifndef TYPECUDA_H_
#define TYPECUDA_H_

#include <inttypes.h>

#define DTYPE float

typedef enum type_node_t { FCONNECTION, PERCEPTRON } type_node;

typedef struct buffer_t {
    uint32_t size;
    DTYPE * propagation_calculated;
    DTYPE * propagation_valid;
    DTYPE * back_propagation;
} buffer;


typedef struct node_t {
    type_node type;
    uint32_t indice;
} node;

typedef struct FC_t {
    DTYPE * matrix;
} FC;

typedef struct PCPTR_t {
    DTYPE * bias;
} PCPTR;



#endif

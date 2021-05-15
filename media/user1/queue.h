#ifndef QUEUE_H
#define QUEUE_H

#include <stdint.h>

typedef struct queue Queue;

int isEmpty(Queue *q);

void Init(Queue **q);

void Enqueue(Queue *q, uint32_t value);

uint32_t Dequeue(Queue *q);

void Clear(Queue **q);

#endif /* QUEUE_H */

#include "queue.h"
#include <stdlib.h>

struct node {
    uint32_t value;
    struct *next;
};

struct queue {
    struct node *front;
    struct node *back;
};

int isEmpty(Queue *q) {
    return (q->front == NULL);
}

void Init(Queue **q) {
    Queue *temp = (Queue *) malloc(sizeof(Queue));
    if(temp == NULL)
        exit(1);
    temp->front = NULL;
    temp->back = NULL;
    *q = temp;
}

void Enqueue(Queue *q, uint32_t value) {
    struct node *temp = (struct node *) malloc(sizeof(struct node));
    if(temp == NULL)
        exit(1);
    temp->value = value;
    temp->next = NULL;

    if (q->front == NULL) {
        q->front = temp;
        q->back = temp;
    } else {
        q->back->next = temp;
        q->back = temp;
    }
}


uint32_t Dequeue(Queue *q) {
    struct node *temp = q->front;

    uint32_t value = q->front->value;
    q->front = q->front->next;

    free(temp);
    return value;
}

void Clear(Queue **q) {
    if (q == NULL)
        return;
    Queue *temp = *q;
    while (!isEmpty(temp)) {
        Dequeue(temp);
    }
    free(temp);
}

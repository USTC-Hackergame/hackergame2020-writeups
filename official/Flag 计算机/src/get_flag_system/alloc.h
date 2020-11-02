#ifndef ALLOC_H
#define ALLOC_H

#include "int.h"

extern char _heap;
static char *hbreak = &_heap;

static void *sbrk(size_t size)
{
    char *ptr = hbreak;
    for (size_t i = 0; i < size; i++)
        ptr[i] = 0;
    hbreak += size;
    return ptr;
}

static void free(void)
{
    hbreak = &_heap;
}

#endif

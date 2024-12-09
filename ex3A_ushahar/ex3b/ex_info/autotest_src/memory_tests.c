#include <stddef.h>
#include <stdlib.h>
#include "memory_tests.h"

void* __real_realloc(void*, size_t);
void* __real_malloc(size_t);
void* __real_calloc(size_t, size_t);

unsigned int fail_realloc_after = 0;
unsigned int fail_malloc_after = 0;

void* __wrap_realloc(void* p, size_t size){
    if (fail_realloc_after)
    {
        if (fail_realloc_after-- == 1)
        {
            return NULL;
        }
    }
    return __real_realloc(p, size);
}

void* __wrap_malloc(size_t size){
    if (fail_malloc_after)
    {
        if (fail_malloc_after-- == 1)
        {
            return NULL;
        }
    }
    return __real_malloc(size);
}

void* __wrap_calloc(size_t n, size_t size){
    if (fail_malloc_after)
    {
        if (fail_malloc_after-- == 1)
        {
            return NULL;
        }
    }
    return __real_calloc(n, size);
}

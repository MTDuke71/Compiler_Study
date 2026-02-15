#include <stdio.h>
#include <stdlib.h>

int global_var = 42;  // data section

int main() {
    int stack_var;    // stack
    int* heap_var = malloc(sizeof(int));  // heap

    printf("Text (code):   %p\n", (void*)main);
    printf("Data (global): %p\n", (void*)&global_var);
    printf("Heap:          %p\n", (void*)heap_var);
    printf("Stack:         %p\n", (void*)&stack_var);

    free(heap_var);
    return 0;
}

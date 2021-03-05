
#include <lkl_host.h> 

int kfuzz_printf(const char* fmt, ...);
int lkl_main(int (*cb)(void), void (*local_print)(const char* s, int len)) {
    lkl_host_ops.print = local_print;

    if (lkl_start_kernel == NULL) {
        kfuzz_printf("kernel function link error");
        return 1;
    }

    int ret = lkl_start_kernel(&lkl_host_ops, "mem=50M");
    if (ret < 0) {
        kfuzz_printf("start failed: ");
        kfuzz_printf("%s\n", lkl_strerror(ret));
        return ret;
    }
    kfuzz_printf("started\n");

    ret = cb();
    lkl_sys_halt();
    return ret;
}

// *** beg of fuzzer.c ***

void drop_slab(void);
int fuzz_main(void) {
    // some other fuzzing code, but not so important to reproduce bug
    drop_slab();
}

// *** end of fuzzer.c ***
// *** beg of main.c ***
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>

FILE *kernel_log = NULL;

void local_print(const char *s, int len) {
    fprintf(kernel_log, "%.*s", len, s);
}

int kfuzz_printf(const char* fmt, ...) {
    int n;
    va_list args;

    va_start(args, fmt);
    n = vprintf(fmt, args);
    va_end(args);

    return n;
}


int main() {

    kernel_log = fopen("kernel.log", "w");
    if (kernel_log == NULL) {
        return 1;
    }

    lkl_main(fuzz_main, local_print);

    if (kernel_log != NULL) {
        fclose(kernel_log);
        kernel_log = NULL;
    }
}



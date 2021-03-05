
build:
	gcc lkl_bug_cpu.c -Ilinux/tools/lkl/include -Llinux/tools/lkl/lib -llkl -o build/lkl

build-idle:
	gcc lkl_bug_cpu_idle.c -Ilinux/tools/lkl/include -Llinux/tools/lkl/lib -llkl -o build/lkl

reproduce:
	gdb -ex "source ./reproduce.py" ./build/lkl


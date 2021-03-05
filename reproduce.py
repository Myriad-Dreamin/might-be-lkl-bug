
import gdb # pylint: disable=all

gdb.execute('set environment LD_PRELOAD ./linux/tools/lkl/lib/liblkl.so')

yellow = '\033[1;33m'
cyan = '\033[1;36m'
reset_color = '\033[0;0m'

gdb.execute("set pagination off")
gdb.execute("set confirm off")

class Handler(object):
    def __init__(self):
        self.signal_emitted = False

    def stop_handler(self, event):
        gdb.execute("set scheduler-locking on") # to avoid parallel signals in other threads
        stop_signal = getattr(event, 'stop_signal', None)
        if stop_signal is None:
            return False

        self.signal_emitted = True
        print(f"{cyan}[exited] SIG {stop_signal}{reset_color}")
        return True

h = Handler()
gdb.events.stop.connect(h.stop_handler)

t = 0
while not h.signal_emitted:
    t += 1
    print(f"{yellow}restart {t} time(s){reset_color}")
    gdb.execute('r < idle.in')
print("bug reproduced...")

# Case1:
# SIGSEGV
# Thread 1 "lkl_cpu" received signal SIGSEGV, Segmentation fault.
# [exited] SIG SIGSEGV
# set_next_entity (cfs_rq=0x7ffff7bed2a0 <runqueues+32>, se=0x0) at kernel/sched/fair.c:4158
# 4158		if (se->on_rq) {
# bug reproduced...

# Case2:
# Deadlock
# 0x00007ffff617a7c6 in futex_abstimed_wait_cancelable (private=0, abstime=0x0, expected=0, futex_word=0x5555557574f0) at ../sysdeps/unix/sysv/linux/futex-internal.h:205
# 205	../sysdeps/unix/sysv/linux/futex-internal.h: No such file or directory.
# bug reproduced...
# (gdb) info threads
#   Id   Target Id         Frame 
# * 1    Thread 0x7ffff7fd4240 (LWP 19306) "lkl_cpu" 0x00007ffff617a7c6 in futex_abstimed_wait_cancelable (private=0, abstime=0x0, expected=0, futex_word=0x5555557574f0) at ../sysdeps/unix/sysv/linux/futex-internal.h:205
#   2    Thread 0x7ffff6169700 (LWP 19307) "lkl_cpu" 0x00007ffff742dc36 in tick_nohz_idle_stop_tick () at kernel/time/tick-sched.c:969
#   3    Thread 0x7ffff7ff4740 (LWP 19308) "lkl_cpu" 0x00007ffff638e33a in timer_helper_thread (arg=<optimized out>) at ../sysdeps/unix/sysv/linux/timer_routines.c:89
#   5    Thread 0x7ffff5167700 (LWP 19310) "lkl_cpu" 0x00007ffff617a7c6 in futex_abstimed_wait_cancelable (private=0, abstime=0x0, expected=0, futex_word=0x7ffff0000e20) at ../sysdeps/unix/sysv/linux/futex-internal.h:205
#   6    Thread 0x7ffff4966700 (LWP 19311) "lkl_cpu" 0x00007ffff617a7c6 in futex_abstimed_wait_cancelable (private=0, abstime=0x0, expected=0, futex_word=0x7fffe8000b20) at ../sysdeps/unix/sysv/linux/futex-internal.h:205
#   7    Thread 0x7fffecdff700 (LWP 19312) "lkl_cpu" 0x00007ffff617a7c6 in futex_abstimed_wait_cancelable (private=0, abstime=0x0, expected=0, futex_word=0x7fffe8000c70) at ../sysdeps/unix/sysv/linux/futex-internal.h:205
#   8    Thread 0x7fffe7fff700 (LWP 19313) "lkl_cpu" 0x00007ffff617a7c6 in futex_abstimed_wait_cancelable (private=0, abstime=0x0, expected=0, futex_word=0x7fffe8000dc0) at ../sysdeps/unix/sysv/linux/futex-internal.h:205
#   9    Thread 0x7fffe77fe700 (LWP 19314) "lkl_cpu" 0x00007ffff617a7c6 in futex_abstimed_wait_cancelable (private=0, abstime=0x0, expected=0, futex_word=0x7fffe8000f10) at ../sysdeps/unix/sysv/linux/futex-internal.h:205
#   10   Thread 0x7fffe6ffd700 (LWP 19315) "lkl_cpu" 0x00007ffff617a7c6 in futex_abstimed_wait_cancelable (private=0, abstime=0x0, expected=0, futex_word=0x7fffe8001060) at ../sysdeps/unix/sysv/linux/futex-internal.h:205
#   11   Thread 0x7fffe67fc700 (LWP 19316) "lkl_cpu" 0x00007ffff617a7c6 in futex_abstimed_wait_cancelable (private=0, abstime=0x0, expected=0, futex_word=0x7fffe80011b0) at ../sysdeps/unix/sysv/linux/futex-internal.h:205
#   12   Thread 0x7fffe5ffb700 (LWP 19317) "lkl_cpu" 0x00007ffff617a7c6 in futex_abstimed_wait_cancelable (private=0, abstime=0x0, expected=0, futex_word=0x7fffe8001300) at ../sysdeps/unix/sysv/linux/futex-internal.h:205
#   13   Thread 0x7fffe57fa700 (LWP 19318) "lkl_cpu" 0x00007ffff617a7c6 in futex_abstimed_wait_cancelable (private=0, abstime=0x0, expected=0, futex_word=0x7fffe8001450) at ../sysdeps/unix/sysv/linux/futex-internal.h:205
#   14   Thread 0x7fffe4ff9700 (LWP 19319) "lkl_cpu" 0x00007ffff617a7c6 in futex_abstimed_wait_cancelable (private=0, abstime=0x0, expected=0, futex_word=0x7fffe80015a0) at ../sysdeps/unix/sysv/linux/futex-internal.h:205
#   15   Thread 0x7fffdffff700 (LWP 19320) "lkl_cpu" 0x00007ffff617a7c6 in futex_abstimed_wait_cancelable (private=0, abstime=0x0, expected=0, futex_word=0x7fffe80016f0) at ../sysdeps/unix/sysv/linux/futex-internal.h:205
#   16   Thread 0x7fffdf7fe700 (LWP 19321) "lkl_cpu" 0x00007ffff617a7c6 in futex_abstimed_wait_cancelable (private=0, abstime=0x0, expected=0, futex_word=0x7fffe8001840) at ../sysdeps/unix/sysv/linux/futex-internal.h:205
#   18   Thread 0x7fffdeffd700 (LWP 19323) "lkl_cpu" 0x00007ffff617a7c6 in futex_abstimed_wait_cancelable (private=0, abstime=0x0, expected=0, futex_word=0x7fffe8001990) at ../sysdeps/unix/sysv/linux/futex-internal.h:205
#   19   Thread 0x7fffde7fc700 (LWP 19324) "lkl_cpu" 0x00007ffff617a7c6 in futex_abstimed_wait_cancelable (private=0, abstime=0x0, expected=0, futex_word=0x7fffe80019c0) at ../sysdeps/unix/sysv/linux/futex-internal.h:205
#   20   Thread 0x7fffddffb700 (LWP 19325) "lkl_cpu" 0x00007ffff617a7c6 in futex_abstimed_wait_cancelable (private=0, abstime=0x0, expected=0, futex_word=0x7fffe8001b10) at ../sysdeps/unix/sysv/linux/futex-internal.h:205
#   21   Thread 0x7fffdd7fa700 (LWP 19326) "lkl_cpu" 0x00007ffff617a7c6 in futex_abstimed_wait_cancelable (private=0, abstime=0x0, expected=0, futex_word=0x7fffe8001c60) at ../sysdeps/unix/sysv/linux/futex-internal.h:205
#   22   Thread 0x7fffdcff9700 (LWP 19327) "lkl_cpu" 0x00007ffff617a7c6 in futex_abstimed_wait_cancelable (private=0, abstime=0x0, expected=0, futex_word=0x7fffe0001b50) at ../sysdeps/unix/sysv/linux/futex-internal.h:205
# (gdb) backtrace 
# #0  0x00007ffff617a7c6 in futex_abstimed_wait_cancelable (private=0, abstime=0x0, expected=0, futex_word=0x5555557574f0) at ../sysdeps/unix/sysv/linux/futex-internal.h:205
# #1  do_futex_wait (sem=sem@entry=0x5555557574f0, abstime=0x0) at sem_waitcommon.c:111
# #2  0x00007ffff617a8b8 in __new_sem_wait_slow (sem=sem@entry=0x5555557574f0, abstime=0x0) at sem_waitcommon.c:181
# #3  0x00007ffff617a929 in __new_sem_wait (sem=sem@entry=0x5555557574f0) at sem_wait.c:42
# #4  0x00007ffff73def64 in sem_down (sem=0x5555557574f0) at lib/posix-host.c:128
# #5  0x00007ffff73e64d8 in lkl_cpu_get () at arch/lkl/kernel/cpu.c:104
# #6  0x00007fffffffda80 in ?? ()
# #7  0x0000000000000000 in ?? ()



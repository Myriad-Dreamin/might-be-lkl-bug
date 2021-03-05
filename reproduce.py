
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

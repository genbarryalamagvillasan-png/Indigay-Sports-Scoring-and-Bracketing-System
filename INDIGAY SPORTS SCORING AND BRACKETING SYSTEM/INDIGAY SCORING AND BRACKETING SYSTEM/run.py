import os, sys, time, subprocess, pathlib

watch_dir = pathlib.Path(__file__).parent.resolve()
entry_file = watch_dir / "main.py"

last_mtimes = {}
p = None

def get_mtimes():
    mtimes = {}
    for path, _, files in os.walk(watch_dir):
        for f in files:
            if f.endswith(".py"):
                full = os.path.join(path, f)
                mtimes[full] = os.path.getmtime(full)
    return mtimes

while True:
    mtimes = get_mtimes()
    if mtimes != last_mtimes:
        last_mtimes = mtimes
        if p:
            p.terminate()
            time.sleep(0.3)
            if p.poll() is None:
                p.kill()
        print("Restarting...")
        p = subprocess.Popen([sys.executable, str(entry_file)])
    time.sleep(1)

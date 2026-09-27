
import os
import gc

s = os.statvfs('/')

total = s[0] * s[2]
free = s[0] * s[3]
print(os.uname())
print(f"Total: {total/1024:.1f} KB")
print(f"Free : {free/1024:.1f} KB")
print(gc.mem_free())


for f in os.listdir('/'):
    st = os.stat(f)
    print(f, st[6])

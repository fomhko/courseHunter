from core import notify

from courselist import courselist
import threading
threads = []
for i in courselist:
    t1 = threading.Thread(target = notify, args = (i,))
    threads.append(t1)
if __name__ == '__main__':
    for t in threads:

        t.start()




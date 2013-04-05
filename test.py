from tasks import add, minus, multi_minus
import random
import time


a, b = random.randint(1, 100), random.randint(1,100)
print add(a,b)
#print add.apply_async(args=(5,4)).get()
add.delay(a, b, False)

def benchmark():
    now = time.time()
    for i in xrange(3000):
        minus.delay(3, 2)

    then = time.time()
    print then - now

    multi_minus.delay(3,2,3000)

    that = time.time()
    print that - then

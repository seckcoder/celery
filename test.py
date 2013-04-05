from tasks import add, minus
import random


a, b = random.randint(1, 100), random.randint(1,100)
print add(a,b)
#print add.apply_async(args=(5,4)).get()
add.delay(a, b, False)

minus.delay(3, 2)

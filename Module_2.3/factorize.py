from multiprocessing import Pool, cpu_count
from datetime import datetime
import math


def factorize(*numbers):
    denominators = {}
    for number in numbers:
        this_denominator = []
        for i in range(1, number+1):
            if number % i == 0:
                this_denominator.append(i)
        denominators[number] = this_denominator
    return denominators


def test_sync_vs_async():
    test_start = datetime.now()
    factors = factorize(128, 255, 99999, 10651060)
    sync_time = datetime.now()-test_start
    print(f"1 thread execution time: {sync_time}")
    test_start = datetime.now()
    pool = Pool(cpu_count())
    pool.apply_async(func=factorize, args=(128, 255, 99999, 10651060))
    async_time = datetime.now()-test_start
    print(f"{cpu_count()} threads execution time: {async_time}")
    print(
        f"Multithreading is {round(sync_time / async_time, 1)} times faster.\n")
    return factors


factors = test_sync_vs_async()
a = factors.get(128)
b = factors.get(255)
c = factors.get(99999)
d = factors.get(10651060)
assert a == [1, 2, 4, 8, 16, 32, 64, 128]
assert b == [1, 3, 5, 15, 17, 51, 85, 255]
assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
             380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

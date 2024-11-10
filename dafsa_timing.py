import random
import time

import matplotlib.pyplot as plt
import numpy as np

from readerdeleter.build.dafsa import DAFSA

alphabet = "+abcdefghijklmnopqrstuvwxyz"


def gen_star_up_to(n):
    if n == 0:
        return ""

    for a in alphabet:
        if random.random() < 0.1:
            yield a
        for tail in gen_star_up_to(n - 1):
            yield a + tail


def time_func(func):
    times = []
    def wrapper(*args, **kwargs):
        f = func(*args, **kwargs)
        t1 = time.time()
        for _ in f:
            times.append(time.time() - t1)
        return times

    return wrapper


@time_func
def generate_words(dafsa, limit, time_spacing, word_len=20):
    n = 0
    for word in gen_star_up_to(word_len):
        # skip half of all possible words
        if random.random() < 0.01:
            continue
        dafsa.add_word(word)

        n += 1
        if n % time_spacing == 0:
            print('generated', n)
            yield True

        if n >= limit:
            break

    dafsa.finish()
    return dafsa


@time_func
def check_words(dafsa, limit, time_spacing, word_len=20):
    n = 0
    for word in gen_star_up_to(word_len):
        dafsa.is_word(word)

        n += 1
        if n % time_spacing == 0:
            print('checked', n)
            yield True

        if n >= limit:
            break
    return False


def main():

    n = 2000000
    points = 400
    freq = n // points

    read_fac = 1
    
    x = np.linspace(0, n, points)

    dafsa = DAFSA()
    gen_times = generate_words(dafsa, n, freq)
    read_times = check_words(dafsa, n*read_fac, freq*read_fac)

    _, (ax1, ax2) = plt.subplots(2, 1)
    ax1.plot(x, gen_times)
    ax2.plot(x*read_fac, read_times)

    ax1.set_title("generation time")
    ax1.set_ylabel("time (s)")
    ax2.set_title("access time")
    ax2.set_xlabel("# of calls")
    ax2.set_ylabel("time (s)")

    plt.show()


if __name__ == "__main__":
    main()

import random
import time

import matplotlib.pyplot as plt
import numpy as np

from readerdeleter.build.dafsa import DAFSA

alphabet = "abcxyz"


def gen_star_up_to(n):
    if n == 0:
        return ""

    for a in alphabet:
        yield a
        for tail in gen_star_up_to(n - 1):
            yield a + tail


def time_func(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        ret = func(*args, **kwargs)
        return time.time() - t1, ret

    return wrapper


@time_func
def generate_words(limit, word_len=20):
    dafsa = DAFSA()
    n = 0
    for word in gen_star_up_to(word_len):
        # skip half of all possible words
        if random.random() < 0.01:
            continue
        dafsa.add_word(word)

        n += 1
        if n % 10000 == 0:
            print(n)

        if n >= limit:
            break

    dafsa.finish()
    return dafsa


@time_func
def check_words(dafsa, limit, word_len=20):
    n = 0
    for word in gen_star_up_to(word_len):
        dafsa.is_word(word)

        n += 1
        if n % 100000 == 0:
            print(n)

        if n >= limit:
            break


def main():

    size_limits = np.linspace(0, 100000, 20)
    gen_times = []
    read_times = []

    for lim in size_limits:
        t1, dafsa = generate_words(lim)
        t2 = check_words(dafsa, lim * 10)
        gen_times.append(t1)
        read_times.append(t2)

    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.plot(size_limits, gen_times)
    ax2.plot(size_limits * 100, read_times)

    ax1.set_title("generation time")
    ax1.set_ylabel("time (s)")
    ax2.set_title("access time")
    ax2.set_xlabel("# of calls")
    ax2.set_ylabel("time (s)")

    plt.show()


if __name__ == "__main__":
    main()

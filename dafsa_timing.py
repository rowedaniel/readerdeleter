import random
import time

import matplotlib.pyplot as plt
import numpy as np

from readerdeleter.build.dafsa import DAFSA
from readerdeleter.gaddag import generate_GADDAG_words

alphabet = "@ABCDEFGHIJKLMNOPQRSTUVWXYZ"


t = time.time()
with open("resources/sample_wordlist_processed.txt", "r") as file:
    words = [word.strip() for word in file.readlines() if 'z' not in word]
    words += [(word[:random.randint(0, 9)] + 'z' + word[random.randint(0, 9):]) for word in words]
    words += [(word[:random.randint(0, 9)] + 'z' + word[random.randint(0, 9):]) for word in words]
    words = generate_GADDAG_words(words)
print("generated all words from file, took", time.time() - t)



def get_words():
    for word in words:
        yield word


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
def generate_words(dafsa, limit, time_spacing):
    n = 0
    for word in get_words():
        dafsa.add_word(word)

        n += 1
        if n % time_spacing == 0:
            print('added', n)
            yield True

        if n >= limit:
            break

    dafsa.finish()
    return dafsa


@time_func
def check_words(dafsa, limit, time_spacing):
    n = 0
    for word in get_words():
        dafsa.is_word(word)

        n += 1
        if n % time_spacing == 0:
            print('checked', n)
            yield True

        if n >= limit:
            break
    return False


def main():

    n = 1900000
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

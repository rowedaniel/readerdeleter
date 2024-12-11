import time
from .build.dafsa import DAFSA

def generate_GADDAG_words(words):
    dafsa_words = [
        (s[: p+ 1][::-1] + "@" + s[p + 1 :]).upper() for s in words for p in range(len(s))
        ]
    dafsa_words.sort()
    return dafsa_words

def generate_GADDAG(words):
    dafsa_words = generate_GADDAG_words(words)
    t = time.time()
    dafsa_words.sort()

    dafsa = DAFSA()
    t = time.time()
    dafsa.add_words(dafsa_words)
    dafsa.finish()
    return dafsa

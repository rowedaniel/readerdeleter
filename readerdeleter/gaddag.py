import time
from .build.dafsa import DAFSA

type GADDAG = DAFSA

def generate_GADDAG_words(words: list[str]) -> list[str]:
    dafsa_words = [
        (s[: p+ 1][::-1] + "@" + s[p + 1 :]).upper() for s in words for p in range(len(s))
        ]
    dafsa_words.sort()
    return dafsa_words

def generate_GADDAG(words: list[str]) -> DAFSA:
    dafsa_words = generate_GADDAG_words(words)
    t = time.time()
    dafsa_words.sort()

    dafsa = DAFSA()
    t = time.time()
    dafsa.add_words(dafsa_words)
    dafsa.finish()
    return dafsa

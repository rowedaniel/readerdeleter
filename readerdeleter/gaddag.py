import time
from readerdeleter.build.dafsa import DAFSA

def generate_GADDAG_words(words: list[str]) -> list[str]:
    dafsa_words = [
        (s[: p+ 1][::-1] + "@" + s[p + 1 :]).upper() for s in words for p in range(len(s))
        ]
    dafsa_words.sort()
    return dafsa_words

def generate_GADDAG(words: list[str]) -> DAFSA:
    dafsa_words = generate_GADDAG_words(words)
    print("sorting")
    t = time.time()
    dafsa_words.sort()
    print("done in", time.time() - t)

    dafsa = DAFSA()
    t = time.time()
    print("adding", len(dafsa_words), "words ( starting at t =", t, ")")
    i = 0
    for word in dafsa_words:
        dafsa.add_word(word)
        i += 1
        if i % 1000 == 0:
            print("at", i, "time =", time.time())
    dafsa.finish()
    print("done in", time.time() - t)
    return dafsa

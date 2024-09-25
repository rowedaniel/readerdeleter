import random

from readerdeleter.build.dafsa import DAFSA

def test_empty():
    dafsa = DAFSA()
    assert not dafsa.is_word("")
    dafsa.add_word("")
    assert dafsa.is_word("")

def test_positive():
    dafsa = DAFSA()
    dafsa.add_word("tests")
    assert dafsa.is_word("tests")


def test_negative():
    dafsa = DAFSA()
    dafsa.add_word("tests")
    assert not dafsa.is_word("foo")


def test_partial():
    dafsa = DAFSA()
    dafsa.add_word("test")
    assert not dafsa.is_word("tests")
    assert not dafsa.is_word("tes")


def test_multiple():
    dafsa = DAFSA()
    print("adding words")
    dafsa.add_word("test")
    dafsa.add_word("testes")
    dafsa.add_word("tests")
    dafsa.add_word("xenomorph")
    print("\n\ntesting words")
    assert not dafsa.is_word("tes")
    assert dafsa.is_word("test")
    assert dafsa.is_word("tests")
    assert dafsa.is_word("testes")
    assert dafsa.is_word("xenomorph")


def test_random():
    dafsa = DAFSA()

    alphabet = "abcd"

    words = [
        "".join(random.choice(alphabet) for _ in range(random.randint(2, 10)))
        for _ in range(100)
    ]
    words.sort()

    nonwords = [
        "".join(random.choice(alphabet) for _ in range(random.randint(2, 10)))
        for _ in range(100)
    ]
    nonwords = [word for word in nonwords if word not in words]

    for word in words:
        dafsa.add_word(word)

    for word in words:
        assert dafsa.is_word(word)
    for word in nonwords:
        assert not dafsa.is_word(word)

import random

from readerdeleter.build.dafsa import DAFSA


def test_empty():
    dafsa = DAFSA()
    assert not dafsa.is_word("")
    dafsa.add_word("")
    assert dafsa.is_word("")


def test_positive():
    dafsa = DAFSA()
    dafsa.add_word("TESTS")
    assert dafsa.is_word("TESTS")


def test_negative():
    dafsa = DAFSA()
    dafsa.add_word("TESTS")
    assert not dafsa.is_word("foo")


def test_partial():
    dafsa = DAFSA()
    dafsa.add_word("TEST")
    assert not dafsa.is_word("TESTS")
    assert not dafsa.is_word("TES")


def test_multiple():
    dafsa = DAFSA()
    dafsa.add_word("TEST")
    dafsa.add_word("TESTES")
    dafsa.add_word("TESTS")
    dafsa.add_word("XENOMORPH")
    assert not dafsa.is_word("TES")
    assert dafsa.is_word("TEST")
    assert dafsa.is_word("TESTS")
    assert dafsa.is_word("TESTES")
    assert dafsa.is_word("XENOMORPH")

def test_plus():
    words = [
        "ET@STS",
        "SET@TS",
        "T@EST",
        "T@E@TS",
        "T@ESTS",
        ]
    dafsa = DAFSA()
    for word in words:
        dafsa.add_word(word)
    for word in words:
        assert dafsa.is_word(word)


def test_random():
    dafsa = DAFSA()

    alphabet = "@ABCDXYZ"

    words = [
        "".join(random.choice(alphabet) for _ in range(random.randint(2, 10)))
        for _ in range(1000)
    ]
    words.sort()

    nonwords = [
        "".join(random.choice(alphabet) for _ in range(random.randint(2, 10)))
        for _ in range(1000)
    ]
    nonwords = [word for word in nonwords if word not in words]

    for word in words:
        dafsa.add_word(word)

    for word in words:
        assert dafsa.is_word(word)
    for word in nonwords:
        assert not dafsa.is_word(word)

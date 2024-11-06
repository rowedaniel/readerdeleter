import random

from readerdeleter.gaddag import generate_GADDAG

def test_empty():
    gaddag = generate_GADDAG([])
    assert not gaddag.is_word("")

def test_one():
    gaddag = generate_GADDAG(["a"])
    assert gaddag.is_word("a+")

def test_two():
    gaddag = generate_GADDAG(["am"])
    assert gaddag.is_word("a+m")
    assert gaddag.is_word("ma+")

def test_three():
    gaddag = generate_GADDAG(["can"])
    assert gaddag.is_word("c+an")
    assert gaddag.is_word("ac+n")
    assert gaddag.is_word("nac+")

def test_random():
    words = [''.join(random.choice('abcd') for _ in range(4)) for _ in range(10)]
    gaddag = generate_GADDAG(words)
    for word in words:
        for i in range(1,len(word)):
            assert gaddag.is_word(word[:i][::-1] + "+" + word[i:])

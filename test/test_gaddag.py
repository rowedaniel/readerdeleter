import random

from readerdeleter.gaddag import generate_GADDAG

def test_empty():
    gaddag = generate_GADDAG([])
    assert not gaddag.is_word("")

def test_one():
    gaddag = generate_GADDAG(["A"])
    assert gaddag.is_word("A@")

def test_two():
    gaddag = generate_GADDAG(["AM"])
    assert gaddag.is_word("A@M")
    assert gaddag.is_word("MA@")

def test_three():
    gaddag = generate_GADDAG(["CAN"])
    assert gaddag.is_word("C@AN")
    assert gaddag.is_word("AC@N")
    assert gaddag.is_word("NAC@")

def test_random():
    words = [''.join(random.choice("ABCD") for _ in range(4)) for _ in range(10)]
    gaddag = generate_GADDAG(words)
    for word in words:
        for i in range(1,len(word)):
            assert gaddag.is_word(word[:i][::-1] + "@" + word[i:])

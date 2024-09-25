from readerdeleter.build.dafsa import DAFSA


def test_dafsa_positive():
    dafsa = DAFSA()
    dafsa.add_word("tests")
    assert dafsa.is_word("tests")


def test_dafsa_negative():
    dafsa = DAFSA()
    dafsa.add_word("tests")
    assert not dafsa.is_word("foo")


def test_dafsa_partial():
    dafsa = DAFSA()
    dafsa.add_word("test")
    assert not dafsa.is_word("tests")
    assert not dafsa.is_word("tes")


def test_dafsa_multiple():
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

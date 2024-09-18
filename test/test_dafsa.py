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

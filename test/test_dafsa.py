from readerdeleter.build.dawg import DAWG


def test_dawg_positive():
    dawg = DAWG()
    dawg.insert_word("tests")
    assert dawg.is_word("tests")


def test_dawg_negative():
    dawg = DAWG()
    dawg.insert_word("tests")
    assert not dawg.is_word("foo")


def test_dawg_partial():
    dawg = DAWG()
    dawg.insert_word("test")
    assert not dawg.is_word("tests")
    assert not dawg.is_word("tes")

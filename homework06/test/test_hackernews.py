# type: ignore
import hackernews


def test_clear():
    assert hackernews.clean("A") == "A"
    assert hackernews.clean("A, B, C") == "A B C"
    assert hackernews.clean("A.a()") == "Aa"


def test_get_weight():
    assert hackernews.get_weight("never") == 2
    assert hackernews.get_weight("maybe") == 1
    assert hackernews.get_weight("good") == 0
    assert hackernews.get_weight("simple") == "Invalid labelsimple"

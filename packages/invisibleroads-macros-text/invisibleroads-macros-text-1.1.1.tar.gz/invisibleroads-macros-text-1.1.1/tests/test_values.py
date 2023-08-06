import pickle
from invisibleroads_macros_text import unicode_safely


def test_unicode_safely():
    assert unicode_safely(b'x') == 'x'
    assert unicode_safely(1) == 1
    assert pickle.loads(unicode_safely(pickle.dumps({}))) == {}

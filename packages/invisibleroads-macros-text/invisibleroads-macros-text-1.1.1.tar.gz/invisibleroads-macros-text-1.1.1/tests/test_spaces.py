from invisibleroads_macros_text import (
    compact_whitespace)


def test_compact_whitespace():
    assert compact_whitespace('  x  y  z  ') == 'x y z'

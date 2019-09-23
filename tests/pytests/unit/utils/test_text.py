from js_routes.utils.text import replace


def test_replace():
    assert replace('this ; is a | test', [(';', '-'), ('|', '--')]) == 'this - is a -- test'

from hammuon import __version__

from hammuon.quick_sort import quickSort

print(quickSort([8, 12, 55, -12]))

def test_version():
    assert __version__ == '0.1.1'

"""
Basic tests for DataShear package.
"""

import datashear


def test_version():
    """Test that version is defined."""
    assert hasattr(datashear, '__version__')
    assert isinstance(datashear.__version__, str)


def test_author():
    """Test that author is defined."""
    assert hasattr(datashear, '__author__')
    assert isinstance(datashear.__author__, str)
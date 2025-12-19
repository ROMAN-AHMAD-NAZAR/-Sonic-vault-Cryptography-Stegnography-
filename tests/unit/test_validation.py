def test_validation_nonempty():
    from src.utils.validation import is_nonempty_str
    assert is_nonempty_str('x')
    assert not is_nonempty_str('')

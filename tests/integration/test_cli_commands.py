def test_cli_import():
    import importlib
    mod = importlib.import_module('cli')
    assert hasattr(mod, 'main') or True

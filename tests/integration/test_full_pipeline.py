def test_full_pipeline_imports():
    # Simple integration smoke test for imports
    import src
    from src.core.sonic_vault import SonicVault
    sv = SonicVault()
    assert sv.run() == "running"

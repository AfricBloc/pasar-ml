from shared.config.settings import settings

def test_settings_load():
    """Ensure shared settings loads ENVIRONMENT."""
    assert settings.ENVIRONMENT is not None

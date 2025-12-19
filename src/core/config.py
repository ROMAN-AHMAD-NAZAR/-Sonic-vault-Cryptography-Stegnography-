"""Configuration handling (placeholder)."""

DEFAULTS = {
    "sample_rate": 44100,
    "bit_depth": 16,
}

class Config:
    def __init__(self, overrides=None):
        self.values = dict(DEFAULTS)
        if overrides:
            self.values.update(overrides)

    def get(self, key, default=None):
        return self.values.get(key, default)

# Ensure repository root is on sys.path so `from app...` imports work in tests
import os
import sys

# Set API key for tests before importing app modules
os.environ.setdefault("API_KEY", "test-key")

# Put repo root on sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Clear cached settings to pick up the test API_KEY
try:
    from app.core.config import get_settings
    get_settings.cache_clear()  # type: ignore[attr-defined]
except Exception:
    # If import fails here, tests that import app will trigger it later.
    pass

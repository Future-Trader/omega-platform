from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

API = ROOT / "apps" / "api"

APP = API / "app"

AUTH = APP / "auth"

SECURITY = APP / "security"

MODELS = APP / "models"

SCHEMAS = APP / "schemas"

TESTS = API / "tests"
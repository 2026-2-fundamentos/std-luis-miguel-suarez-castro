import importlib
from pathlib import Path

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
IS_PROFESSOR = any((path / ".PROFESSOR").exists() for path in ACTIVITY_DIR.parents)
CODE_DIR = ACTIVITY_DIR / ("professor" if IS_PROFESSOR else "src")


def answer(name, monkeypatch):
    monkeypatch.syspath_prepend(str(ACTIVITY_DIR))

    candidates = [f"{CODE_DIR.name}.main", "main"]
    last_error = None

    for module_name in candidates:
        try:
            module = importlib.import_module(module_name)
            return getattr(module, name)()
        except ModuleNotFoundError as exc:
            last_error = exc
            if exc.name not in {module_name, module_name.rsplit(".", 1)[0]}:
                raise

    raise last_error


def test_01(monkeypatch):
    assert answer("pregunta_01", monkeypatch) == "Hola mundo cruel!"


def test_02(monkeypatch):
    assert answer("pregunta_02", monkeypatch) == "Hello cruel world!"

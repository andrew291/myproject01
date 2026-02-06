from pathlib import Path

def load_dotenv(path: str = ".env") -> None:
    """
    Minimal .env loader (stdlib only).
    Supports KEY=VALUE lines, ignores comments and blanks.
    Does not overwrite existing environment variables.
    """
    env_path = Path(path)
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        import os
        os.environ.setdefault(key, value)

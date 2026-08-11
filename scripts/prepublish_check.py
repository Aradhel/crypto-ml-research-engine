from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOCKED_NAMES = {".env", "trades.db", "ml_model.pkl", "control.json", "heartbeat.json", "id_rsa", "id_ed25519"}
BLOCKED_SUFFIXES = {".db", ".sqlite", ".sqlite3", ".pkl", ".pickle", ".joblib", ".log", ".pem", ".key", ".p12", ".pfx"}
TEXT_SUFFIXES = {".py", ".md", ".txt", ".yml", ".yaml", ".json", ".html", ".css", ".example"}
SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|api[_-]?secret|secret[_-]?key|client[_-]?secret|access[_-]?token|auth[_-]?token|bearer[_-]?token|password|passwd|passphrase)\s*[=:]\s*['\"]?[^'\"\s]{8,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)authorization\s*:\s*bearer\s+[A-Za-z0-9._-]{16,}"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\b(?:xox[baprs]-)[A-Za-z0-9-]{20,}\b"),
]


def main() -> int:
    problems = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.name in BLOCKED_NAMES or path.suffix.lower() in BLOCKED_SUFFIXES:
            problems.append(f"blocked file: {path.relative_to(ROOT)}")
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                problems.append(f"possible credential: {path.relative_to(ROOT)}")
                break
    if problems:
        print("PUBLICATION BLOCKED")
        print("\n".join(f"- {item}" for item in problems))
        return 1
    print("Publication check passed: no blocked runtime or credential files found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Earthdata credential helpers.

Credentials are loaded from environment variables first, then from a local
untracked text file. Values are never logged by these helpers.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path


DEFAULT_CREDENTIAL_FILE = Path("nasa earthdata acc info.txt")


@dataclass(frozen=True)
class EarthdataCredentials:
    username: str
    password: str


def load_earthdata_credentials(path: Path = DEFAULT_CREDENTIAL_FILE) -> EarthdataCredentials:
    username = os.environ.get("EARTHDATA_USERNAME")
    password = os.environ.get("EARTHDATA_PASSWORD")
    if username and password:
        return EarthdataCredentials(username=username, password=password)

    if not path.exists():
        raise FileNotFoundError(
            "Earthdata credentials not found. Set EARTHDATA_USERNAME/EARTHDATA_PASSWORD "
            f"or create the untracked file {path}."
        )

    text = path.read_text(encoding="utf-8")
    username = _extract_value(text, ("username", "user", "login", "email"))
    password = _extract_value(text, ("password", "pass"))
    if not username or not password:
        raise ValueError(
            "Could not parse Earthdata credentials. Use lines like "
            "username: YOUR_USERNAME and password: YOUR_PASSWORD."
        )
    return EarthdataCredentials(username=username, password=password)


def _extract_value(text: str, labels: tuple[str, ...]) -> str | None:
    label_pattern = "|".join(re.escape(label) for label in labels)
    pattern = re.compile(rf"^\s*(?:earthdata[_ -]?)?(?:{label_pattern})\s*[:=]\s*(.+?)\s*$", re.I)
    for line in text.splitlines():
        match = pattern.match(line)
        if match:
            return match.group(1).strip().strip("'\"")
    return None

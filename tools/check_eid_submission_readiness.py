"""Strict EID submission readiness checker with human-info warnings."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SUBMISSION = ROOT / "docs" / "submission_eid"
MANUSCRIPT = SUBMISSION / "manuscript_eid.md"
COVER = SUBMISSION / "cover_letter_eid.md"
STATEMENTS = SUBMISSION / "author_statements.md"
APPENDIX = SUBMISSION / "supplements" / "Appendix_methods_eid.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _words(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", text))


def _section(text: str, start: str, end: str) -> str:
    lower = text.lower()
    s = lower.find(start.lower())
    if s < 0:
        return ""
    e = lower.find(end.lower(), s + len(start))
    return text[s:e] if e >= 0 else text[s:]


def _title(text: str) -> str:
    match = re.search(r"\*\*Title:\*\*\s*\n(.+?)(?:\n\n|\n\*\*)", text, re.S)
    return " ".join(match.group(1).split()) if match else ""


def _running_head(text: str) -> str:
    match = re.search(r"\*\*Running head:\*\*\s*(.+)", text)
    return match.group(1).strip() if match else ""


def _references(text: str) -> int:
    ref_block = _section(text, "## References", "## Figure Legends")
    return len(re.findall(r"^\d+\.", ref_block, flags=re.M))


def _coverage_numerator_denominator(text: str) -> bool:
    return bool(re.search(r"\b\d+\s*/\s*\d+\b", text))


def _check_figures(failures: list[str]) -> None:
    for name in ["Figure_1.tif", "Figure_2.tif", "Figure_3.tif"]:
        path = SUBMISSION / "figures" / name
        if not path.exists():
            failures.append(f"Missing figure: {path}")
            continue
        with Image.open(path) as image:
            dpi = image.info.get("dpi", (0, 0))
            width_inches = image.size[0] / float(dpi[0] or 1)
            if min(dpi) < 300:
                failures.append(f"{name} below 300 dpi: {dpi}")
            if width_inches < 5:
                failures.append(f"{name} below 5 inches wide: {width_inches:.2f}")
    schematic = SUBMISSION / "figures" / "Appendix_Figure_model_schematic.tif"
    if not schematic.exists():
        failures.append("Missing model schematic figure")


def check_readiness(strict: bool = False) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    warnings: list[str] = []
    manuscript = _read(MANUSCRIPT)
    cover = _read(COVER)
    statements = _read(STATEMENTS)
    appendix = _read(APPENDIX)

    if not manuscript:
        failures.append("Missing manuscript_eid.md")
        return failures, warnings

    title = _title(manuscript)
    if not title:
        failures.append("Missing title")
    if ":" in title:
        failures.append("Title contains a colon")
    if "EU/EEA" in title:
        failures.append("Title uses EU/EEA instead of spelling out place")
    if "European Union and European Economic Area" not in title:
        failures.append("Title does not spell out European Union and European Economic Area")

    running = _running_head(manuscript)
    if not running:
        failures.append("Missing running head")
    elif len(running) > 50:
        failures.append(f"Running head exceeds 50 characters: {len(running)}")

    abstract = _section(manuscript, "## ABSTRACT", "---\n\n## TEXT")
    abstract_words = _words(abstract) - 1 if abstract else 0
    if abstract_words <= 0:
        failures.append("Missing abstract")
    elif abstract_words > 150:
        failures.append(f"Abstract exceeds 150 words: {abstract_words}")

    body = _section(manuscript, "### Introduction", "## Acknowledgments")
    body_words = _words(body)
    if body_words > 3500:
        failures.append(f"Main text exceeds 3500 words: {body_words}")

    refs = _references(manuscript)
    if refs > 50:
        failures.append(f"References exceed 50: {refs}")
    elif refs > 40:
        warnings.append(f"References exceed conservative 40-reference target: {refs}")

    required_phrases = {
        "one-sentence summary": "One-sentence summary",
        "strobe/reporting statement": "STROBE",
        "ethics statement": "institutional review was not required",
        "ai disclosure": "Artificial intelligence",
        "data/code availability": "Data and code",
        "author biography": "Biographical sketch",
        "orcid": "ORCID",
        "corresponding email": "Email:",
        "eid author checklist": "Author Checklist",
    }
    combined = "\n".join([manuscript, cover, statements, appendix])
    for label, phrase in required_phrases.items():
        if phrase.lower() not in combined.lower():
            failures.append(f"Missing {label}: {phrase}")

    if not _coverage_numerator_denominator(manuscript):
        failures.append("No exact numerator/denominator coverage text in manuscript")

    forbidden_patterns = {
        "primacy language": r"\b(first|to our knowledge)\b",
        "live dashboard claim": r"live dashboard",
        "operational predictor claim": r"operational predictor",
        "incorrect Boone attribution": r"\bBoone\b",
        "unsupported causal phrase": r"caused by",
    }
    for label, pattern in forbidden_patterns.items():
        if re.search(pattern, combined, flags=re.I):
            failures.append(f"Forbidden/needs manual removal: {label}")

    required_files = [
        SUBMISSION / "tables" / "table1_model_inputs.csv",
        SUBMISSION / "tables" / "appendix_surveillance_quality_sensitivity.csv",
        SUBMISSION / "tables" / "appendix_country_influence.csv",
        SUBMISSION / "tables" / "appendix_calibration_localization.csv",
        SUBMISSION / "tables" / "appendix_detectability_screen.csv",
        SUBMISSION / "reports" / "surveillance_quality_sensitivity.md",
        SUBMISSION / "reports" / "country_influence.md",
        SUBMISSION / "reports" / "calibration_localization.md",
        SUBMISSION / "reports" / "detectability_screen.md",
        SUBMISSION / "reproducibility_manifest.md",
        APPENDIX,
        SUBMISSION / "manuscript_eid.docx",
        SUBMISSION / "cover_letter_eid.docx",
        SUBMISSION / "author_statements.docx",
    ]
    for path in required_files:
        if not path.exists():
            failures.append(f"Missing required artifact: {path}")

    table1 = SUBMISSION / "tables" / "table1_model_inputs.csv"
    if table1.exists():
        import pandas as pd

        columns = set(pd.read_csv(table1).columns)
        needed = {"source", "training_range_min", "training_range_max", "missingness_rule", "lag_used"}
        if not needed.issubset(columns):
            failures.append("Table 1 lacks source/range/missingness/lag columns")

    _check_figures(failures)

    if "suitability inquiry" not in _read(SUBMISSION / "submission_guide_eid.md").lower():
        warnings.append("Optional EID suitability-inquiry decision not documented")
    if "mailing address" in combined.lower():
        warnings.append("Mailing address/phone still require human portal confirmation")
    if "zenodo.20150542" in combined:
        warnings.append("DOI must be verified or updated after final archive/version")
    if strict and failures:
        return failures, warnings
    return failures, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    failures, warnings = check_readiness(strict=args.strict)
    for warning in warnings:
        print(f"WARN: {warning}")
    if failures:
        print("EID readiness: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("EID readiness: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

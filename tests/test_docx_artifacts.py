"""Regression test for final EID DOCX artifacts."""

from __future__ import annotations

from tools.check_docx_artifacts import check_docx_artifacts


def test_docx_artifacts_are_structurally_ready() -> None:
    assert check_docx_artifacts() == []

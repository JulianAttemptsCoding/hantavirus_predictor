"""Tests for the strict EID submission readiness checker."""

from __future__ import annotations

from tools.check_eid_submission_readiness import check_readiness


def test_strict_eid_submission_readiness_passes_without_failures() -> None:
    failures, warnings = check_readiness(strict=True)

    assert failures == []
    assert all("mailing address" in warning.lower() or "doi" in warning.lower() for warning in warnings)

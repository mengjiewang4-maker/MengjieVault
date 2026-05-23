"""Dose matrix helpers for EBL planning."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DosePoint:
    """One EBL dose condition."""

    label: str
    dose_percent: int
    pec: str
    purpose: str


def default_dose_matrix() -> list[DosePoint]:
    """Return a conservative PEC-on dose matrix template."""

    return [
        DosePoint("D1", 20, "on", "low-dose boundary"),
        DosePoint("D2", 25, "on", "candidate low dose"),
        DosePoint("D3", 30, "on", "candidate dose"),
        DosePoint("D4", 35, "on", "candidate dose"),
        DosePoint("D5", 40, "on", "near previous lower bound"),
        DosePoint("D6", 45, "on", "comparison only"),
    ]


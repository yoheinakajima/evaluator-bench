"""Drift guard for paper section 5.5.

Every number cited in paper/draft.md section 5.5 must match what the
repository data computes. If the data changes without the paper being
updated (or vice versa), this test fails.
"""
from pathlib import Path

from bench.load import load
from bench.paper_stats import section_5_5_stats

ROOT = Path(__file__).resolve().parents[1]


def _stats():
    return section_5_5_stats(load(strict=False))


def _paper():
    return (ROOT / "paper" / "draft.md").read_text()


def test_section_5_5_signal_counts_match_paper():
    s = _stats()
    text = _paper()
    assert f"{s['n_for']} for and {s['n_against']} against" in text
    assert f"{s['n_spans']} of {s['n_signals']} with a quoted span" in text


def test_section_5_5_source_counts_match_paper():
    s = _stats()
    text = _paper()
    assert (f"Of {s['n_sources']} unique sources cited, "
            f"{s['n_self']} are the evaluators' own statements and "
            f"{s['n_tier1']} are filings or funder indexes") in text


def test_section_5_5_unevidenced_counts_match_paper():
    s = _stats()
    text = _paper()
    u = s["unevidenced"]
    assert f"{u['against_interest']} of 192 assessments are unevidenced" in text
    assert f"under primary only, {u['primary']} are" in text
    assert f"{u['standard']} of 192 assessments are unevidenced" in text


def test_section_5_5_held_and_resolved_match_paper():
    s = _stats()
    text = _paper()
    assert f"{s['n_held']} assessments are held at a supportable anchor" in text
    assert (f"{s['n_resolved']} conflicts between a floor and a cap "
            "are resolved by a named rule") in text


def test_section_5_5_funding_and_means_match_paper():
    s = _stats()
    text = _paper()
    assert f"{s['n_funding_le2']} of 24 score 2 or below on funding" in text
    assert f"differ by at most {s['max_leads_std_mean_diff_2dp']}" in text


def test_section_5_5_bands_match_paper():
    s = _stats()
    text = _paper()
    b = s["bands"]
    assert (f"{b['clear']} of the {s['n_ranked']} ranked organizations are in the clear band, "
            f"{b['conditional']} carry a conditional floor") in text
    assert f"and {b['disqualifying']} carry a disqualifying floor" in text


def test_section_5_5_stale_numbers_are_gone():
    text = _paper()
    for stale in ("159 for and 159 against",
                  "275 of 318 with a quoted span",
                  "Of 181 unique sources cited",
                  "100 are the evaluators' own statements and 21 are filings",
                  "under primary only, 171 are",
                  "Ten assessments are held at a supportable anchor",
                  "differ by at most 0.05",
                  "Eleven of 24 score 2 or below on funding"):
        assert stale not in text, f"stale number still in paper: {stale!r}"

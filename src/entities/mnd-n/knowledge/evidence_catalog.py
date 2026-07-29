"""Reviewed evidence metadata used by MND-N's counselor guidance layer.

The catalog stores bounded summaries, not clinical rules. Guidance code should
preserve each source's population and scope when presenting a research note.
"""

EVIDENCE_CATALOG = {
    "interaction_balance": {
        "title": "Marital processes predictive of later dissolution: behavior, physiology, and health",
        "authors": "Gottman & Levenson",
        "year": 1992,
        "url": "https://doi.org/10.1037/0022-3514.63.2.221",
        "evidence_type": "longitudinal observational study",
        "scope": "married-couple conflict interactions; not a universal counseling ratio",
    },
    "perma_profiler": {
        "title": "The PERMA-Profiler: A brief multidimensional measure of flourishing",
        "authors": "Butler & Kern",
        "year": 2016,
        "url": "https://doi.org/10.5502/ijw.v6i3.526",
        "evidence_type": "measure development and validation",
        "scope": "wellbeing assessment across PERMA domains; not a treatment protocol",
    },
    "positive_psychology_meta_analysis": {
        "title": "Positive psychology interventions: a meta-analysis of randomized controlled studies",
        "authors": "Bolier et al.",
        "year": 2013,
        "url": "https://doi.org/10.1186/1471-2458-13-119",
        "evidence_type": "systematic review and meta-analysis",
        "scope": "small average effects with substantial heterogeneity and variable study quality",
    },
    "slow_breathing_meta_analysis": {
        "title": "Effects of voluntary slow breathing on heart rate and heart rate variability",
        "authors": "Laborde et al.",
        "year": 2022,
        "url": "https://doi.org/10.1016/j.neubiorev.2022.104711",
        "evidence_type": "systematic review and meta-analysis",
        "scope": "slow breathing and vagally mediated HRV; not proof of a specific psychological diagnosis",
    },
    "adaptive_wearable_biofeedback": {
        "title": "Enabling Adaptive Cardio-Respiratory Biofeedback Training on Ubiquitous Hand-Worn Devices",
        "authors": "Yu et al.",
        "year": 2026,
        "url": "https://doi.org/10.1145/3772318.3790488",
        "evidence_type": "CHI controlled user study",
        "scope": "adaptive hand-worn biofeedback; early research rather than clinical treatment validation",
    },
    "resilience_neural_signatures": {
        "title": "Neural signatures of human psychological resilience driven by acute stress",
        "authors": "Watanabe et al.",
        "year": 2026,
        "url": "https://doi.org/10.1073/pnas.2524075123",
        "evidence_type": "multimodal acute-stress study",
        "scope": "group-level fMRI, EEG, and peripheral physiology findings; not individual diagnosis",
    },
}


def get_evidence(*source_ids: str) -> list[dict]:
    """Return copies of reviewed evidence records in the requested order."""
    return [dict(EVIDENCE_CATALOG[source_id], id=source_id) for source_id in source_ids]

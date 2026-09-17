import math

from experiments.wti_prior_window_sensitivity import PRIORS, PriorProfile, _configuration_id


def test_prior_profile_inverse_gamma_moments():
    profile = PriorProfile("finite", 3.0, 0.8)
    assert profile.mean == 0.4
    assert abs(profile.sd - 0.4) < 1e-12


def test_baseline_prior_has_infinite_standard_deviation():
    baseline = next(profile for profile in PRIORS if profile.name == "baseline")
    assert baseline.alpha == 2.0
    assert baseline.beta == 0.1
    assert math.isinf(baseline.sd)


def test_configuration_id_changes_with_computational_budget():
    base = dict(
        windows=(63, 252),
        chains=4,
        n_iter=20_000,
        burn_in=4_000,
        seed=17,
        contract_id="x",
    )
    first = _configuration_id(**base)
    second = _configuration_id(**{**base, "n_iter": 40_000})
    assert first != second

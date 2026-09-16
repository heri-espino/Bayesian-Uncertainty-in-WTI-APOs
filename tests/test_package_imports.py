import bayesian_asian_options as bao
from bayesian_asian_options import (
    accelerated_pricing,
    asian_futures_pricing,
    asian_pricing,
    barchart_apo,
    barchart_cl,
    bayesian_gbm,
    rates,
    synthetic_validation,
    volatility_regimes,
    wti_apo_pricing,
    wti_first_nearby,
    wti_yahoo,
    wti_yahoo_futures,
)


def test_canonical_package_namespace_is_importable() -> None:
    assert bao.__version__ == "0.1.0"
    assert callable(bayesian_gbm.random_walk_metropolis_gbm)
    assert callable(asian_pricing.asian_arithmetic_call_mc)
    assert callable(accelerated_pricing.asian_arithmetic_call_mc_chunked)
    assert callable(asian_futures_pricing.asian_futures_arithmetic_call_mc)
    assert callable(barchart_apo.build_apo_panel)
    assert callable(barchart_cl.load_barchart_cl_strip)
    assert callable(wti_first_nearby.assign_first_nearby_contract)
    assert callable(wti_apo_pricing.wti_average_price_option_mc)
    assert callable(wti_apo_pricing.wti_apo_cross_section_mc)
    assert callable(volatility_regimes.realized_volatility)
    assert callable(wti_yahoo.prepare_wti_model_sample)
    assert callable(wti_yahoo_futures.reconstruct_first_nearby_history)
    assert callable(rates.treasury_curve_on_or_before)
    assert callable(synthetic_validation.risk_neutral_martingale_check)

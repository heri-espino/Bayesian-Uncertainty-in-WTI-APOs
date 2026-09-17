import numpy as np
import pandas as pd

from experiments.wti_mc_convergence import _select_contract, _split_fixing_state


def test_split_fixing_state_uses_status_when_available():
    frame = pd.DataFrame(
        {
            "fixing_status": ["realized", "remaining", "remaining"],
            "fixing_date": ["2026-09-01", "2026-09-02", "2026-09-03"],
            "settlement": [70.0, 71.0, 72.0],
        }
    )
    realized, forwards, times = _split_fixing_state(frame, pd.Timestamp("2026-09-01"))
    assert np.array_equal(realized, np.array([70.0]))
    assert np.array_equal(forwards, np.array([71.0, 72.0]))
    assert np.all(times > 0)


def test_select_contract_defaults_to_largest_gap():
    frame = pd.DataFrame(
        {
            "contract_id": ["a", "b"],
            "fb_minus_pm": [0.001, -0.004],
        }
    )
    selected = _select_contract(frame, None)
    assert selected["contract_id"] == "b"

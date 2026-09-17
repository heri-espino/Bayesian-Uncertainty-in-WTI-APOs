# Curran near-zero volatility stability

The Curran geometric-conditioning benchmark solves for an exercise boundary in the conditioning variable. A purely standard-deviation-based bracket becomes numerically inappropriate as sigma approaches zero: an economically ordinary strike displacement can correspond to an enormous number of geometric-mean standard deviations.

The implementation therefore solves the conditional-mean boundary in log space using `logsumexp` and expands the bracket on an absolute log-price scale as well as the local statistical scale. This preserves the deterministic sigma -> 0 limit without replacing small positive volatility by zero.

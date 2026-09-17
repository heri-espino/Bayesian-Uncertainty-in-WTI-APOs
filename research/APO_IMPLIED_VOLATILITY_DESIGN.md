# APO-implied volatility design

The empirical repository already contains the inputs needed to infer a risk-neutral volatility from WTI Average Price Option settlements under the paper's pricing model: the APO settlement, strike/type, realized first-nearby fixings, remaining CL futures fixing curve, and discount factor.

For each contract-date observation, the experiment solves

\[
C_{\mathrm{Curran}}(\sigma_Q)=C_{\mathrm{settlement}}.
\]

This is an **APO-implied** risk-neutral volatility, not an independent external volatility source. The experiment therefore separates inversion from evaluation:

- individual contract IVs describe the cross-sectional implied-volatility shape;
- leave-one-contract-out calibration excludes the target option before estimating one date-level scalar sigma_Q;
- call-to-put / put-to-call transfer calibrates on one option type and evaluates the other.

The comparison against the paper's historical-volatility baseline is therefore meaningful as an out-of-sample cross-sectional pricing exercise, while still being labeled correctly as internally APO-implied. Vanilla CL options would provide an additional independent Q-volatility benchmark, but are not required for the present experiment.

# Model methodology: what the estimates mean

## Model 1: constant returns to scale (default)

The structural expression is

\[
Y_t = A K_t^{\alpha} L_t^{1-\alpha}.
\]

The implemented ordinary least squares regression is

\[
\log(Y_t/L_t) = \log A + \alpha\log(K_t/L_t) + \varepsilon_t.
\]

`alpha_capital` is the OLS slope, `beta_labour` is **defined** to be `1 - alpha_capital`, and `scale_factor = exp(intercept)`. The constant-returns restriction is an **assumption**, not a test result. Elasticities are unrestricted in the software: a statistically fitted value outside the theoretically usual interval [0, 1] is reported, not silently clipped.

## Model 2: unrestricted returns to scale

\[
\log Y_t = \log A + \alpha\log K_t + \beta\log L_t + \varepsilon_t.
\]

Both slopes are estimated; the reported `returns_to_scale_sum` is `alpha + beta`. This is descriptive log-linear OLS and not a causal or structural productivity estimate.

## Base year normalization

`--base-year 2012` (for example) divides every capital, labour and output observation by that variable's **own** value in 2012. Each input becomes an index of 1 in that year. The model is fitted to those indexes; hence `scale_factor` is in indexed units and is **not numerically comparable** to a model fitted in physical/monetary units. Fitted model rows include normalized values so observed and predicted are comparable on one scale.

Normalization does not fix incompatible definitions, production boundaries, nominal/real differences or mismeasured labour. Without `--base-year`, input values retain their supplied units.

## Model outputs

- In-sample predicted **level**: `exp(log A + alpha log K + beta log L)`.
- `residual_output`: observed minus predicted output in supplied or normalized units.
- `residual_log_output`: log observed minus log predicted.
- `r_squared_level` and `r_squared_log`: separately calculated, **in-sample**, not interchangeable.
- `rmse_level` and `mae_level`: in-sample output-scale errors.

No confidence intervals or p-values are supplied: default OLS formula assumptions about serial correlation, cointegration, endogeneity and measurement quality would make naive inference misleading for many macroeconomic time series. Do not interpret fit statistics as out-of-sample forecast validation.

## Economic validation checklist

Before estimating a real Canada model:

1. Determine whether the target is **aggregate Canada**, **manufacturing Canada**, or a narrower sector. Never mix them implicitly.
2. Use productive **capital stock/services**, not investment flow in its place without an explicit modelling argument.
3. Decide whether labour should be **hours**, **persons**, or an adjusted labour input. These are not interchangeable.
4. Use a coherent output concept (e.g. real value added vs real gross output), including compatible deflator/base and industry coverage.
5. Choose annualization intentionally: **mean** for some stocks/rates, **last** for some year-end stocks, **sum** for some additive flows. Confirm each vector's frequency, units and seasonal adjustment.
6. Inspect missing/suppressed data, partial final years, revisions, vintage effects, changes in classification, chain-linking, and calendar-vs-fiscal years.
7. Decide whether log-level regression is statistically appropriate for nonstationary data; consider cointegration and robustness diagnostics before reporting results.
8. Retain the precise source ZIPs, vector identifiers, metadata, and conversion choices with the output.

## Scope of reliability

The numerical implementation is validated with synthetic known-coefficient cases, input-validation edge cases, and offline component tests. This verifies software behavior, **not** the empirical validity of a Canadian production function. The original manuscript described in the archived code was not supplied and is not treated as a verified reference.

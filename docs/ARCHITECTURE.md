# Architecture and trust boundaries

## Public data boundary

Only deterministic synthetic OHLCV is accepted by the demo pipeline. The public
repository has no exchange client and no credential-loading code. Generated
research artifacts live under `artifacts/demo`.

## Temporal boundary

Each fold trains on an expanding historical window. Six 4-hour rows are removed
between train and test as an embargo. Test rows never enter the corresponding
training window.

## Execution boundary

Signals are paper observations. The project has no order types, authenticated
HTTP calls or account state. The dashboard reads generated JSON and exposes a
health status; it cannot mutate a portfolio.

## Conservative assumptions

- Round-trip cost is subtracted from every selected observation.
- When both stop and target are inside one candle, stop is assumed first.
- Missing or unresolved paths are not silently counted as wins.


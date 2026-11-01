"""Demand forecasting models and evaluation.

Three models are provided so that the app can compare them and pick the best
one per product:

* Moving Average          - simple baseline
* Holt-Winters (additive) - trend + weekly seasonality, implemented from scratch
* Random Forest           - ML model on lag / calendar features (scikit-learn)
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

MODEL_NAMES = ["Moving Average", "Holt-Winters", "Random Forest"]


# --------------------------------------------------------------------------- #
# Metrics
# --------------------------------------------------------------------------- #
def mae(actual, pred) -> float:
    return float(np.mean(np.abs(np.asarray(actual) - np.asarray(pred))))


def rmse(actual, pred) -> float:
    return float(np.sqrt(np.mean((np.asarray(actual) - np.asarray(pred)) ** 2)))


def wmape(actual, pred) -> float:
    """Weighted MAPE (%) - safe when some actual values are zero."""
    actual = np.asarray(actual, dtype=float)
    denom = np.sum(np.abs(actual))
    if denom == 0:
        return float("nan")
    return float(np.sum(np.abs(actual - np.asarray(pred))) / denom * 100)


# --------------------------------------------------------------------------- #
# Models  (each takes a pd.Series indexed by daily dates and returns np.ndarray)
# --------------------------------------------------------------------------- #
def moving_average_forecast(series: pd.Series, horizon: int, window: int = 14) -> np.ndarray:
    level = float(series.tail(window).mean())
    return np.full(horizon, level)


def holt_winters_forecast(
    series: pd.Series,
    horizon: int,
    season_length: int = 7,
    alpha: float = 0.25,
    beta: float = 0.02,
    gamma: float = 0.15,
) -> np.ndarray:
    """Additive Holt-Winters (triple exponential smoothing)."""
    y = series.to_numpy(dtype=float)
    n = len(y)
    if n < 2 * season_length:
        return moving_average_forecast(series, horizon)

    # Initialise level, trend and seasonal components from the first two seasons.
    level = y[:season_length].mean()
    trend = (y[season_length : 2 * season_length].mean() - y[:season_length].mean()) / season_length
    seasonal = list(y[:season_length] - level)

    for i in range(season_length, n):
        s = seasonal[i - season_length]
        last_level = level
        level = alpha * (y[i] - s) + (1 - alpha) * (level + trend)
        trend = beta * (level - last_level) + (1 - beta) * trend
        seasonal.append(gamma * (y[i] - level) + (1 - gamma) * s)

    forecast = [
        level + (h + 1) * trend + seasonal[n - season_length + (h % season_length)]
        for h in range(horizon)
    ]
    return np.clip(np.array(forecast), 0, None)


def _make_features(history: list[float], date: pd.Timestamp) -> list[float]:
    arr = np.asarray(history, dtype=float)
    return [
        arr[-1],
        arr[-7],
        arr[-14],
        arr[-7:].mean(),
        arr[-28:].mean(),
        date.dayofweek,
        date.month,
        date.day,
    ]


def random_forest_forecast(series: pd.Series, horizon: int, seed: int = 42) -> np.ndarray:
    """Random Forest on lag features with recursive multi-step forecasting."""
    min_len = 28 + 30
    if len(series) < min_len:
        return holt_winters_forecast(series, horizon)

    values = series.to_numpy(dtype=float).tolist()
    dates = series.index
    X, y = [], []
    for i in range(28, len(values)):
        X.append(_make_features(values[:i], dates[i]))
        y.append(values[i])

    model = RandomForestRegressor(n_estimators=120, min_samples_leaf=3, random_state=seed, n_jobs=-1)
    model.fit(np.array(X), np.array(y))

    history = values[:]
    preds = []
    next_date = dates[-1]
    for _ in range(horizon):
        next_date = next_date + pd.Timedelta(days=1)
        p = float(model.predict(np.array([_make_features(history, next_date)]))[0])
        p = max(p, 0.0)
        preds.append(p)
        history.append(p)
    return np.array(preds)


MODEL_FUNCS = {
    "Moving Average": moving_average_forecast,
    "Holt-Winters": holt_winters_forecast,
    "Random Forest": random_forest_forecast,
}


def forecast(series: pd.Series, horizon: int, model: str) -> pd.Series:
    """Forecast `horizon` days ahead; returns a Series with future daily dates."""
    if model not in MODEL_FUNCS:
        raise ValueError(f"Unknown model '{model}'. Choose from {MODEL_NAMES}.")
    values = MODEL_FUNCS[model](series, horizon)
    idx = pd.date_range(series.index[-1] + pd.Timedelta(days=1), periods=horizon, freq="D")
    return pd.Series(values, index=idx, name="forecast")


# --------------------------------------------------------------------------- #
# Evaluation
# --------------------------------------------------------------------------- #
@dataclass
class ModelScore:
    model: str
    mae: float
    rmse: float
    wmape: float


def evaluate_models(series: pd.Series, holdout: int = 28) -> pd.DataFrame:
    """Hold out the last `holdout` days, fit every model on the rest and score it."""
    train, test = series.iloc[:-holdout], series.iloc[-holdout:]
    rows = []
    for name, fn in MODEL_FUNCS.items():
        pred = fn(train, holdout)
        rows.append(ModelScore(name, mae(test, pred), rmse(test, pred), wmape(test, pred)).__dict__)
    return pd.DataFrame(rows).sort_values("wmape").reset_index(drop=True)


def best_model(series: pd.Series, holdout: int = 28) -> str:
    return str(evaluate_models(series, holdout).iloc[0]["model"])

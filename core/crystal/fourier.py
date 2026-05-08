from __future__ import annotations

import numpy as np

from core.models import BCell


def noise_profile(series: list[float]) -> dict[str, float]:
    if len(series) < 8:
        return {"energy": 0.0, "stable_ratio": 0.0, "noise_ratio": 0.0}
    values = np.asarray(series, dtype=float)
    spectrum = np.abs(np.fft.rfft(values - values.mean()))
    energy = float(np.sum(spectrum))
    if energy == 0:
        return {"energy": 0.0, "stable_ratio": 1.0, "noise_ratio": 0.0}
    low = float(np.sum(spectrum[: max(1, len(spectrum) // 8)]))
    high = float(np.sum(spectrum[len(spectrum) // 2 :]))
    return {"energy": energy, "stable_ratio": low / energy, "noise_ratio": high / energy}


def fold_noise(cell: BCell, noise_threshold: float = 0.45) -> BCell:
    profile = noise_profile(cell.access_series)
    if profile["noise_ratio"] > noise_threshold:
        cell.trust_score = max(0.0, cell.trust_score - 0.08)
        cell.crystal_state.phase = "purifying"
    elif profile["stable_ratio"] > 0.65 and profile["energy"] > 0:
        cell.trust_score = min(1.0, cell.trust_score + 0.03)
        cell.crystal_state.phase = "reinforced"
    return cell

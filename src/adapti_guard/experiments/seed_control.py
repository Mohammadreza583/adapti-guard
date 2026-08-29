"""
Reproducible seed control for ADAPTI-GUARD experiments.

The Phase 7/8A controlled pipeline (frozen attack stream + explicit
episode schedule + rule-based detector/risk/policy) is currently
fully deterministic. Seeding still records the configured seed and
initializes any available RNG backends so future stochastic
components inherit a single control point.

Do not invent randomness solely to create cross-seed variance.
"""

from __future__ import annotations

import os
import random
from typing import Any


def set_global_seed(seed: int) -> dict[str, Any]:
    """
    Seed all RNG backends that are actually available.

    Returns a provenance dict describing what was seeded.
    """

    if not isinstance(seed, int):
        raise TypeError("seed must be an int")

    provenance: dict[str, Any] = {
        "seed": seed,
        "python_random": True,
        "numpy": False,
        "torch": False,
        "PYTHONHASHSEED": False,
    }

    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    provenance["PYTHONHASHSEED"] = True

    try:
        import numpy as np  # type: ignore

        np.random.seed(seed)
        provenance["numpy"] = True
    except ImportError:
        pass

    try:
        import torch  # type: ignore

        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        provenance["torch"] = True
    except ImportError:
        pass

    return provenance

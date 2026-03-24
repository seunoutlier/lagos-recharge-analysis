# Lagos Groundwater Recharge Analysis

## Identifying optimal rainfall conditions for groundwater recharge using machine learning: Evidence from Lagos megacity

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Key Finding

**Lagos lost 38 percentage points of recharge efficiency at moderate rainfall (150-200mm) between the 1980s and 2010s (p=0.0015). The city's hydrological sweet spot has been paved over.**

![Decadal Shift](figures/Figure_Decadal_Shift.png)

## Discovery Summary

| Decade | Optimal Zone | Peak Efficiency |
|--------|--------------|-----------------|
| 1980s | 150-200 mm | 72.9% |
| 1990s | 200-250 mm | 55.1% |
| 2000s | 200-250 mm | 71.1% |
| 2010s | 300-400 mm | 45.1% |

### Statistical Significance

At 150-200 mm/month rainfall:
- **1980s efficiency:** 72.9%
- **2010s efficiency:** 35.1%
- **Change:** -37.8 percentage points
- **p-value:** 0.0015 (highly significant)

## Installation
```bash
git clone https://github.com/[your-username]/lagos-recharge-analysis.git
cd lagos-recharge-analysis
pip install -r requirements.txt
```

## Usage
```python
from lagos_recharge_analysis import main

results, stats = main("data/lagos_water_balance.xlsx")
```

Or from command line:
```bash
python lagos_recharge_analysis.py data/lagos_water_balance.xlsx
```

## Data

The analysis uses 41 years of monthly water balance data (1980-2020) from Lagos, Nigeria:
- **Records:** 432 monthly observations
- **Variables:** Precipitation, Recharge, Runoff, AET, Interception
- **Source:** WetSpass-M distributed model (Olabode & Comte, 2025)

## Figures

| Figure | Description |
|--------|-------------|
| `Figure_Decadal_Shift.png` | Main figure showing efficiency decline across decades |
| `Figure_Efficiency_Decline.png` | Bar charts of peak efficiency and collapse at 150-200mm |
| `Figure_Temporal_Trends.png` | Time series of efficiency at key precipitation levels |

## Interpretation

**Why the decline?**
- Urbanization → paved surfaces → reduced infiltration
- Compacted soils → lower permeability
- Lost natural drainage → water runs off instead of recharging

**What this means for Lagos:**
1. Historical water management baselines no longer apply
2. Moderate rainfall now causes runoff, not recharge
3. Need 300-400mm rainfall to achieve what 150mm once did
4. Climate adaptation must account for this shift

## Related Publication

Olabode, O. & Comte, J.C. (2025). Long-term groundwater security in the fast-growing coastal megacity of Lagos, Nigeria: insights from distributed recharge simulations. *Hydrological Sciences Journal*. [DOI:10.1080/02626667.2025.2505171](https://doi.org/10.1080/02626667.2025.2505171)

## Presentation

This work was presented at the **Alan Turing Institute PhD Presentation Day** (March 2026).

## Citation
```bibtex
@software{lagos_recharge_analysis,
  author = {[Oluwaseun Franklin Olabode]},
  title = {Lagos Groundwater Recharge Analysis: Identifying Optimal Rainfall Conditions},
  year = {2026},
  url = {https://github.com/[seunoutlier]/lagos-recharge-analysis}
}
```

## License

MIT License

## Contact

- **Author:** [Oluwaseun Franklin Olabode]
- **Email:** [your.email@institution.ac.uk]
- **Institution:** [Your Institution]

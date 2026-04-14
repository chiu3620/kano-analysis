# Kano Analysis

A Python tool for performing **Kano Model** analysis on survey data. It classifies product/service features into Kano categories, computes Satisfaction Increment (SI) and Dissatisfaction Increment (DSI), and generates scatter plots for visualization.

## Overview

The Kano Model classifies features into the following categories based on paired functional/dysfunctional survey questions:

| Code | Category | Description |
|------|----------|-------------|
| **A** | Attractive | Increases satisfaction when present, but no dissatisfaction when absent |
| **O** | One-dimensional | Satisfaction is proportional to the degree of fulfillment |
| **M** | Must-be | Expected by default; absence causes dissatisfaction |
| **I** | Indifferent | Neither satisfying nor dissatisfying |
| **R** | Reverse | Presence causes dissatisfaction |
| **Q** | Questionable | Contradictory response |

## Project Structure

```
kano_analysis/
├── main.py            # Core analysis: reads survey data, classifies features, computes SI/DSI
├── plot.py            # Scatter plot of features on the SI-DSI plane
├── plot_ellipse.py    # Scatter plot with elliptical cluster overlays
└── README.md
```

## Requirements

- Python 3
- `pandas`
- `matplotlib`
- `openpyxl` (for reading/writing `.xlsx` files)

Install dependencies:

```bash
pip install pandas matplotlib openpyxl
```

## Usage

### 1. Run the Kano analysis

```bash
python main.py
```

Reads `raw.xlsx` and outputs `Kano_分析結果.xlsx` containing per-feature classification counts, the dominant Result category, SI, and DSI.

### 2. Generate scatter plot

```bash
python plot.py
```

Produces `kano_plot.png` — a scatter plot of all features on the SI (x-axis) vs DSI (y-axis) plane with quadrant dividers.

### 3. Generate scatter plot with ellipses

```bash
python plot_ellipse.py
```

Produces `kano_plot_ellipse.png` — same as above but with elliptical overlays showing the distribution spread of each Kano category.

## Data Format

### Input: `raw.xlsx`

An Excel file (`.xlsx`) with a sheet named `表單回應 1`. The sheet should contain survey responses with the following column structure:

- **Functional questions** — columns starting with `1. ` and containing a feature name in square brackets, e.g.:
  ```
  1. 如果具備這個功能，你的感受是？ [Feature Name]
  ```
- **Dysfunctional questions** — columns starting with `2. ` and containing the same feature name in square brackets, e.g.:
  ```
  2. 如果不具備這個功能，你的感受是？ [Feature Name]
  ```

Each cell contains one of the following responses (in Traditional Chinese):

| Response | Meaning |
|----------|---------|
| 喜歡 | Like |
| 應該的 | Expect |
| 無所謂 | Neutral |
| 能忍受 | Can tolerate |
| 不喜歡 | Dislike |

### Output: `Kano_outcome.xlsx`

| Column | Description |
|--------|-------------|
| (index) | Feature name |
| A, O, M, I, R, Q | Count of respondents classified into each Kano category |
| Result | The most frequent category for that feature |
| SI | Satisfaction Increment: (A + O) / (A + O + M + I)<br>*Closer to 1 indicates that the presence of the feature greatly increases satisfaction.* |
| DSI | Dissatisfaction Increment: -1 * (O + M) / (A + O + M + I)<br>*Closer to -1 indicates that the absence of the feature causes significant dissatisfaction.* |


## Notes

- The font is set to `Microsoft JhengHei` for rendering Chinese feature names in plots. Change `plt.rcParams['font.family']` if using a different OS or font.
- Quadrant divider lines are placed at the midpoint between the O-cluster max and I-cluster min on each axis.


## References

If you use this tool or methodology in your academic or professional work, please consider referring to the foundational research:

1. **Original Kano Model:** Kano, N., Seraku, N., Takahashi, F., & Tsuji, S. (1984). Attractive quality and must-be quality. *Journal of the Japanese Society for Quality Control*, 14(2), 39-48.
2. **Customer Satisfaction Coefficient (SI/DSI):** Berger, C., Blauth, R., Boger, D., Bolster, C., Burchill, G., DuMouchel, W., ... & Walden, D. (1993). Kano's methods for understanding customer-defined quality. *Center for Quality of Management Journal*, 2(4), 3-36.

## License

This project is open-source and available under the [MIT License](LICENSE).
# TimeManager — probabilistic time-to-completion predictor

## Members:

Anthony Maida amaida@csu.fullerton.edu

Steven Burroughs bishopsscope@csu.fullerton.edu

**Short description (TL;DR)**

TimeManager is a small desktop/web hybrid utility that collects your historical segment completion times and uses a Monte Carlo + linear-regression driven simulation to generate a *distribution* of project completion times. It fits many possible linear trajectories (each a simulation of how average segment duration might evolve), solves for when each trajectory reaches the target number of segments, and reports a range of likely completion times.

---

## Key features

- Stores per-category historical segment times in CSV files under `~/TimeManager/csv_files/`.
- Simulates many possible completion trajectories using repeated sampling from a Gaussian distribution estimated from your historical data.
- Fits multiple linear models (one per simulated trajectory) and shifts them to the current progress point to get candidate completion times.
- Produces a min / max range of predicted completion times and (optionally) plots the candidate trajectories with matplotlib.
- GUI adaptor built with `eel` (JS/HTML frontend) — the Python backend exposes task creation, time-reset, and "next segment" actions.

---

## Quick file map

- `main.py` — Eel adapter and entry point (exposes backend functions to the JS UI).
- `task.py` — Task metadata, CSV loading/saving, and schedule persistence (pickled schedule file).
- `computation.py` — Core modeling, data collection, simulation, line-fitting, plotting, and CSV backup.
- `view/` — (not included here) HTML/CSS/JS files for the `eel` frontend.

---

## How to run (developer quick start)

1. Install dependencies (tested with Python 3.8+):

```bash
pip install numpy scikit-learn matplotlib eel
```

2. Run the app (starts an `eel` GUI server and opens `index.html`):

```bash
python main.py
```

3. In the GUI: create a task (category, name, number of segments). When you begin work, press **Reset Time** to start the timer. Each time you finish a subtask, press **Next Segment**. The system will append the latest segment duration to the category CSV and recompute the simulation and predicted completion-time range.

---

## The modeling approach (technical)

This project uses a *simulation + regression* approach to produce a distribution of time-to-complete estimates. The pipeline is:

1. **Empirical distribution estimation** — take the historical per-segment durations for a category (CSV), compute the sample mean `μ` and sample standard deviation `σ`.

2. **Monte Carlo sampling per trajectory** — repeat `num_lines` times (each is one simulated trajectory):
   - Start with an accumulator `time = 0`.
   - For each segment index `k = 1..num_subtasks`:
     - Add to `time` a random draw of `iterations` independent samples from `N(μ, σ)` and take the *mean* of these `iterations` samples (so each segment advances time by the mean of a small simulated batch). This produces a single `x` value (cumulative time) for that segment.
     - Record the pair `(x, y=k)` where `y` is the number of completed segments at cumulative time `x`.
   - After iterating through all segments you have an array of `(x, y)` pairs that represent the simulated progression of segments vs time for that trajectory.

3. **Fit a linear model for each trajectory** — fit a **linear regression without intercept**, i.e. `y ≈ slope * x` using the simulated `(x, y)` pairs for that trajectory. The code then **overwrites** the fitted intercept to anchor the line at the current observed position `(x_curr, y_curr)` (where `x_curr` is minutes since the task start and `y_curr` is the current subtask index).

4. **Solve for completion time** — for each shifted linear model (a line of the form `y = a * x + b`), solve for `x` when `y = total_segments`. This gives one candidate completion time (in minutes) per simulated trajectory. The set of candidate `x` values form an empirical distribution of completion times.

5. **Report interval** — take the minimum and maximum of those candidate completion times to present a range (a very conservative interval). Optionally display plotted lines and the current point.

**Why the design?**

- Taking the mean of multiple Gaussian draws per segment reduces the noise from single-sample outliers and emphasizes the trajectory of *typical* segment durations.
- Fitting many simulated trajectories and solving them for the target yields a sampling-based estimate of the distribution of completion times (a non-parametric predictive approach).

**Mathematical notes & assumptions**

- The model assumes per-segment durations are i.i.d. and approximately Gaussian; the code uses empirical `μ` and `σ` from the CSV data. If these assumptions are violated (e.g., heavy tails, time-varying segment distributions), predictions will be biased.
- Each simulated trajectory collapses a distribution of per-segment outcomes down to its mean at each step. That reduces extreme variance but also underrepresents tail events.
- The current method returns the min and max completion times observed in simulations (sensitive to outliers). Better uncertainty summaries would use quantiles (e.g., 5th/95th percentile) or credible intervals.

---

## Key classes & main methods (developer view)

### `Task_Information` (`task.py`)
- Holds metadata (category, name, number of segments, display flag, simulation parameters).
- Loads/saves per-category CSV data at `~/TimeManager/csv_files/{category}.csv`.
- `data()` returns the `numpy` array of stored per-segment times (minutes).

### `Schedule` (`task.py`)
- Maintains a list of `Task_Information` objects and persists them with `pickle` at `~/TimeManager/schedule/schedule.pckl`.
- `setup_computation(task_name)` returns a `Computation` instance anchored to the requested task.

### `Computation` (`computation.py`)
- Tracks real-time values: `start_time`, `prev_time`, `conception_time`, `prev_seg`, etc.
- `reset_start_time()` — initialize the timer when a task begins.
- `next_segment()` — primary external call after finishing a subtask: increments subtask number, triggers `running_code()`, and returns a dictionary summarizing results (prev times, range, etc.).
- `running_code()` — executes the full pipeline: collect the latest segment (`get_segment()`), compute minutes since last segment, append to CSV data, run `train_lines_2()`, optionally `plot_lines()`, compute `retrieve_endpoints()` and `return_interval()`, and finally backup CSV.
- `train_lines_2()` — the simulation + per-trajectory linear regression routine described above. It produces `self.lines` (list of fitted `sklearn` LinearRegression objects). Note: `fit_intercept=False` is used and intercept is later set manually to anchor the line at the current observed point.
- `plot_lines()` — convenience plotting of each trajectory and the current position.
- Output of interest: `self.min_end_point` and `self.max_end_point` — the minimum and maximum predicted completion times (in minutes) based on the simulated trajectories.

---

## Example usage flow

1. Create a task with a `category` (used for CSV filename) and `num_segments`.
2. Open the GUI and press **Reset Time** once you start the task; this sets an internal `start_time` reference.
3. After finishing each segment, press **Next Segment**. The application will:
   - Capture the duration of the just-completed segment in minutes and append it to the category's CSV.
   - Re-run the simulation/regression pipeline and update the predicted range for completion time.
   - Optionally plot the simulated progress lines.

---

## Known limitations & potential bugs

- **Empty CSV / insufficient data:** if there is no historical data, `np.mean()` and `np.std()` may produce `nan` and break the sampling. The app should guard for this and require an initial seed dataset or fallback defaults.
- **Distributional assumption:** using a Gaussian for positive-valued time data is sometimes inappropriate (consider log-normal, gamma, or empirical bootstrap instead).
- **Complex roots / numerical edge cases:** `np.roots()` may return complex numbers; the code currently takes min/max across these values without filtering to real, positive roots.
- **Manual intercept assignment:** the code fits with `fit_intercept=False` and *overwrites* intercept_. This is an unusual pattern that can hide modeling issues; consider fitting with intercept or explicitly deriving intercept analytically.
- **Time arithmetic around midnight / DST:** the code attempts to handle AM/PM wrap-around but the logic is brittle. It's safer to use `datetime` arithmetic consistently (`abs((t2 - t1).total_seconds())`) and timezone-aware datetimes if needed.

---

## Concrete improvements (roadmap & ideas)

### Modeling & statistics
- Replace naive Gaussian sampling with **bootstrap resampling** from the empirical per-segment data (non-parametric) or fit a more appropriate positive-valued distribution (log-normal, gamma) and sample from that.
- Instead of taking `min`/`max` as the final interval, report **quantiles** (e.g., 5th / 50th / 95th percentiles) and plot the empirical CDF of predicted completion times.
- Model per-segment heterogeneity: treat the distribution of segment *k* separately (if you have labeled per-segment types), or use hierarchical Bayesian models to allow sharing of strength across segments.
- Use proper uncertainty propagation (e.g., generate full trajectories from sampled per-segment durations instead of sampling means per segment) to capture tail risk.

### Code quality & robustness
- Add unit tests for time arithmetic, root extraction, serialization, and main computations.
- Replace the manual intercept hack: either fit `LinearRegression(fit_intercept=True)` to the simulated `(x, y)` pairs and then shift the model analytically, or derive the intercept from the slope and current point more explicitly.
- Validate input CSVs and handle empty datasets gracefully; provide a guided "seed data" workflow.
- Convert datetimes to timezone-aware objects and handle DST/midnight robustly.
- Filter `np.roots()` results to real-valued, positive roots and handle complex noise robustly.

### UX / Visualization
- Show percentile bands (shaded regions) instead of raw min/max. Add an interactive chart that shows the distribution of completion times.
- Add an option to export a short report (PDF) that summarizes predicted finish date/times with confidence intervals.

### Engineering / deployment
- Containerize the app with Docker and include a CLI entrypoint for scripting.
- Convert the computational module to a library-like interface so it can be imported and tested independently of `eel`.
- Persist time-series history in a lightweight database (SQLite) instead of CSV/pickle for better concurrency and queryability.
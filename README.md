# Once Upon a Dataset
### An Interactive Story-Driven Mortgage Data Experience
**HMDA Historic Data 2007–2017 · CFPB**

> *"The crisis ended. The access gap didn't."*

---

## What This Is

Once Upon a Dataset is an interactive data storytelling app built on 64 million mortgage records from the Consumer Financial Protection Bureau's Home Mortgage Disclosure Act (HMDA) historic dataset (2007–2017).

Rather than presenting raw statistics, the app tells the story of the 2008 financial crisis and its decade-long aftermath through five human characters — each representing a real demographic group whose experience of the housing market was fundamentally different.

---

## Project Structure

```
your-project/
├── hmda_master.parquet       ← HMDA data file (not included, see Data Setup below)
├── Home.py                   ← Entry point — Page 1: Market Overview
├── utils.py                  ← Shared colors, CSS, data loading, chart helpers, character definitions
├── shared.py                 ← Additional styling, character list, and chart/data helpers
├── requirements.txt
├── README.md
├── CHANGELOG.md
├── LICENSE                   ← MIT License (code only)
├── .githooks/                ← Git pre-commit check that blocks large, data, and secret files
├── pages/
│   ├── 1_Stories.py          ← Page 2: Five character story arcs
│   ├── 2_Compare.py          ← Page 3: Side-by-side character comparison
│   └── 3_Explore.py          ← Page 4: Raw data explorer with filters
└── .claude/                  ← Claude Code settings: hook that keeps the assistant inside this folder
```

---

## Pages

| Page | File | Description |
|------|------|-------------|
| **Overview** | `Home.py` | Market-level context — crash & recovery timeline, government intervention, the rising borrower income bar, gender gap analysis, and geographic pulse map |
| **Stories** | `pages/1_Stories.py` | Choose one of five characters and follow their decade through annotated story beats, focused charts, and a character-specific state map |
| **Compare** | `pages/2_Compare.py` | Select any two characters and see their story beats side by side, with a shared volume chart showing how the same market looked from two perspectives |
| **Explore** | `pages/3_Explore.py` | Filter the underlying aggregated data by year, state, loan type, and loan purpose — with live KPIs, a volume trend chart, and a loan type breakdown |

---

## The Five Characters

| Character | Represents | Key Insight |
|-----------|-----------|-------------|
| 🧑🏾 **Marcus** | First-time buyer from underserved community | Minority borrower share nearly halved post-crash and never recovered |
| 👨‍💼 **David** | High-income established buyer | Crisis tightening filtered out competition — advantaging those already stable |
| 🪖 **James** | Military veteran | VA loan share grew 6× (1.7% → 10.6%) as private lenders fled |
| 👩‍👧 **Maria** | First-generation FHA borrower | FHA tripled overnight from 6% to 22% — becoming the market's only floor |
| 🏠 **Sandra** | Existing homeowner refinancing | 67% of 2009 mortgages were refis — the recovery was an illusion until 2014 |

---

## Installation

### System requirements

- **Python** 3.11 or newer
- **Memory:** 16 GB RAM recommended. The app aggregates all 64 million HMDA records into memory on first load, which takes roughly 30–60 seconds. After that the results are cached and pages load instantly.

### 1. Clone or download the project

```bash
cd /path/to/your-project
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your data file

Place `hmda_master.parquet` in the root of the project folder, alongside `Home.py`. See **Data Setup** below.

### 5. Run the app

```bash
streamlit run Home.py
```

The app will open automatically at `http://localhost:8501`.

### 6. Enable the pre-commit check (contributors)

```bash
git config core.hooksPath .githooks
```

This turns on `.githooks/pre-commit`. It blocks any commit that stages a file larger than 10 MB, a data or credential file (`.parquet`, `.env`, `.pem`, `.key`, SSH keys, `secrets.toml` and similar), or content that looks like an API key, token or private key. That keeps the HMDA data file and any secrets out of the repository. The hook needs `python` on your PATH.

---

## Data Setup

This app requires a pre-processed parquet file named `hmda_master.parquet` built from the CFPB's HMDA Historic Data.

### Source

The raw data is publicly available from the CFPB:
- **URL:** https://www.consumerfinance.gov/data-research/hmda/historic-data/
- **Coverage:** 2007–2017 (note: 2012 is not included in the CFPB bulk release due to a schema difference in that year's reporting format)
- **License:** Public domain — U.S. government data

### Building the parquet file

The app expects a single consolidated parquet file with the following key columns:

| Column | Description |
|--------|-------------|
| `as_of_year` | Loan origination year (2007–2017) |
| `loan_purpose_name` | e.g. `Home purchase`, `Refinancing` |
| `loan_type_name` | e.g. `Conventional`, `FHA-insured`, `VA-guaranteed` |
| `applicant_race_name_1` | e.g. `White`, `Black or African American`, `Asian` |
| `applicant_sex_name` | e.g. `Male`, `Female`, `Joint (Male/Female)` |
| `applicant_income_000s` | Applicant income in thousands of dollars |
| `loan_amount_000s` | Loan amount in thousands of dollars |
| `state_abbr` | Two-letter state abbreviation |

To build the parquet, download the annual CSV/TSV files from the CFPB link above and combine them:

```python
import pandas as pd
import glob

files = glob.glob('hmda_raw/*.csv')
df = pd.concat([pd.read_csv(f, low_memory=False) for f in files])
df.to_parquet('hmda_master.parquet', index=False)
```

---

## A Note on 2012 Data

The CFPB's historic HMDA bulk dataset does not include 2012 in the same standardized format as the other years. This is a known, documented limitation of the official data release — not a processing error. External sources (Mortgage Bankers Association) confirm that 2012 was approximately the peak refinancing year of the post-crisis period, with $2.56 trillion in total originations, which is consistent with the trend the data shows across 2011 and 2013.

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `streamlit` | Web app framework and multipage navigation |
| `pandas` | Data loading, aggregation, and filtering |
| `plotly` | Interactive charts (line, bar, choropleth, dual-axis) |
| `pyarrow` | Parquet file reading |

---

## Design System

The app uses a consistent dark editorial aesthetic across all pages, defined in `utils.py`:

- **Fonts:** Playfair Display (headings), Inter (body), JetBrains Mono (data labels)
- **Color palette:** Dark navy background with gold, red, green, blue, and purple accents — each character has a dedicated color
- **Charts:** All built with Plotly, transparent backgrounds, unified hover mode
- **CSS:** Injected via `inject_css()` from `utils.py` — all pages share the same design tokens

---

## Technical Notes

- All data aggregations are computed once on startup and cached with `@st.cache_data` — subsequent interactions are instant
- The app uses Streamlit's native multipage routing — `Home.py` is the entry point and `pages/` contains the remaining pages
- `utils.py` must be in the **root folder** (same level as `Home.py`), not inside `pages/`. Each page file uses `sys.path.insert` to find it
- The app was developed with Python 3.11 and has also been run and tested with Python 3.14 (Streamlit 1.64, pandas 3.0)

---

## Data Citation

> Consumer Financial Protection Bureau. *Home Mortgage Disclosure Act (HMDA) Historic Data, 2007–2017.* Retrieved from https://www.consumerfinance.gov/data-research/hmda/historic-data/

---

## License

- **Code:** [MIT License](LICENSE). You're free to use, modify and share it, including commercially, as long as the copyright notice is kept.
- **Data:** the HMDA data is U.S. government public domain (see Data Citation above). It isn't included in this repository.

# Changelog

## Unreleased — 2026-09-29

### Fixed
- **Data file path no longer depends on the launch folder.** `utils.py` and `shared.py` loaded `hmda_master.parquet` by a bare relative filename, so the app only found it when started from the project folder. Both now build the path from their own location (`DATA_PATH = Path(__file__).parent / 'hmda_master.parquet'`).
  - `utils.py`: `load_all_data()` reads `DATA_PATH`.
  - `shared.py`: `load_data()` defaults to `DATA_PATH` (a different path can still be passed in).
- **App crashed with out-of-memory on first load.** `load_all_data()` in `utils.py` read all 24 columns of the 64.3M-row parquet file, which exceeded available RAM on a 16 GB machine (`ArrowMemoryError` / `Unable to allocate`). It now reads only the 8 columns it uses, and reads the 5 text columns as categoricals (`read_dictionary`). The aggregations and their results are unchanged. All four pages were checked and render without errors.

### Added
- **Claude Code guardrail hook** (`.claude/`). A `PreToolUse` hook stops the Claude Code assistant from reading or writing anything outside the project folder.
  - `.claude/settings.json`: registers the hook for every tool.
  - `.claude/hooks/restrict_paths.py`: checks file-tool paths exactly, and checks shell commands on a best-effort basis (absolute paths, `..` escapes, `~`, `$env:TEMP` and similar). It fails closed if it can't parse a call.
  - `.claude/hooks/test_restrict_paths.py`: 21 allow/deny cases. Run with `python .claude/hooks/test_restrict_paths.py`. Test paths are generic (no personal usernames).
- **Git pre-commit check** (`.githooks/`). Blocks commits that stage:
  - files over 10 MB;
  - data or credential file types (`.parquet`, `.env*`, `.pem`, `.key`, `.p12`/`.pfx`, SSH keys, `credentials.*`/`secrets.*`, `.streamlit/secrets.toml`);
  - content that looks like a secret (private keys, AWS/Google/GitHub/Slack tokens, `sk-...` API keys, hard-coded `password`/`token`/`api_key` values).
  - `.githooks/pre-commit` is a shell wrapper that runs `.githooks/pre_commit.py`. Enable per clone with `git config core.hooksPath .githooks`.
  - `.gitattributes` keeps the hook script's LF line endings so it runs on Windows checkouts.
- **Git repository initialized** on branch `main`, with the pre-commit check enabled.
- **`LICENSE`: MIT License** (copyright Once Upon a Dataset, 2026) for the application code. The README's License section now covers MIT for code and public domain for the HMDA data, replacing the earlier "educational and research use" wording.

### Changed
- **Replaced deprecated `use_container_width=True` with `width='stretch'`** in all 20 `st.plotly_chart` / `st.dataframe` calls (`Home.py` ×6, `pages/1_Stories.py` ×10, `pages/2_Compare.py` ×1, `pages/3_Explore.py` ×3). Streamlit had scheduled the old argument for removal after 2025-12-31.
- `requirements.txt`: raised the minimum to `streamlit>=1.64.0` (the version tested), since older releases don't accept `width='stretch'` on charts.
- `.gitignore`: ignore `__pycache__/`.
- `README.md`: the project structure now lists `shared.py`, `CHANGELOG.md` and `.claude/`. The Technical Notes now say the app has also been tested on Python 3.14 (Streamlit 1.64, pandas 3.0). New "System requirements" (16 GB RAM recommended, 30–60 s first load) and "Enable the pre-commit check" sections.

### Notes
- No API keys or other secrets were found in `utils.py` or `shared.py`.
- `hmda_master.parquet` (614 MB) is git-ignored, and the pre-commit check also blocks it, so it can't be committed by accident. Anyone cloning the repo needs to build it (see README → Data Setup).
- `shared.py` isn't imported by any page (they all use `utils.py`). It's kept as is for now.

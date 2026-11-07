# PathForge AI
### Personalized Career & Skill-Path Recommendation System

PathForge AI is a local-first student project that compares a learner's skills with eight technology career profiles, extracts skills from resumes, prioritises skill gaps, creates a four-week learning plan, and stores assessment history in SQLite.

## What is included
- `app.py` — Streamlit dashboard and workflow
- `engine.py` — skill extraction, matching, role ranking, gap analysis and recommendations
- `data.py` — transparent skill vocabulary and eight role requirement profiles
- `database.py` — SQLite persistence
- `ml_models.py` — reproducible synthetic-data training for Decision Tree readiness and K-Means clustering
- `evaluate.py` — evaluation script; reports metrics from the generated synthetic data
- `resume_parser.py` — PDF, DOCX and TXT resume extraction
- `tests/` — automated tests for core functions
- `data/` — generated demo data and model artefacts are created here when needed

## Run locally (Windows)
1. Install Python 3.10 or later.
2. Extract this ZIP.
3. Open Command Prompt in the `pathforge_ai` folder.
4. Create and activate a virtual environment:

   ```bat
   py -m venv .venv
   .venv\Scripts\activate
   ```
5. Install dependencies:

   ```bat
   pip install -r requirements.txt
   ```
6. Start the application:

   ```bat
   streamlit run app.py
   ```

## Run locally (Linux / macOS)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Run tests and evaluation
```bash
python -m pytest -q
python evaluate.py
```

## Demo login
This version does not require accounts or collect passwords. A user can enter a display name and start an assessment. This is deliberate for a safe, simple undergraduate demonstration. SQLite stores only the display name, assessment summary and skill values locally.

## How the score works
The weighted match score is:

`100 × sum(importance × min(student_level, target_level)) / sum(importance × target_level)`

Each skill level is in the range 0–100. The score is a measure of profile alignment with the project's curated role matrix; it is **not** a probability of getting hired.

## Machine-learning components
- A Decision Tree estimates a three-level readiness label from synthetic training examples.
- K-Means groups synthetic skill profiles for demonstration.
- The app uses the transparent weighted match score as its primary explanation and shows the ML readiness estimate as a secondary signal.
- The generated data are synthetic. Evaluation metrics must not be presented as real-world hiring accuracy.

## Important academic note
The included role weights, synonym dictionary, learning resources and synthetic examples are editable project assumptions. Validate them with your project guide and cite any external datasets or sources you add. Do not claim that the system predicts employment or salary.

## Project structure
```text
pathforge_ai/
├── app.py
├── engine.py
├── data.py
├── database.py
├── resume_parser.py
├── ml_models.py
├── evaluate.py
├── requirements.txt
├── README.md
├── data/
└── tests/
    └── test_engine.py
```

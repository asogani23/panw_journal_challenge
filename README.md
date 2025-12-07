# AI-Powered Journaling CLI (PANW Intern Engineer Challenge)

Author: **Aagam Sogani**  
Role: Palo Alto Networks Product Software Engineer Intern Case Challenge  
Option: **1 – AI-Powered Journaling Logic**

---

## 1. Overview

This repository contains my solution for **Option 1: AI-Powered Journaling Logic**.

The project is a small **command-line journaling tool** that ingests raw, conversational text and tags each entry with mental well-being signals:

- `mood`   – positive / negative / neutral  
- `energy` – low / medium / high  
- `stress` – high / drained / engaged / moderate / unknown  

The focus is **engineering integrity**. I optimized for:

- Clean, readable code split into small modules (`analyzer`, `storage`, `cli`, `tests`).
- A simple, reliable CLI that is easy to run and reason about.
- Using existing tools where they make sense, and writing custom logic only where needed.

### 1.1 Design choices at a glance

- **Sentiment library – `vaderSentiment`**  
  I chose VADER instead of writing my own sentiment model or calling a remote API because:
  - It is **lightweight and offline** (no network calls, no API keys), which fits a CLI tool.
  - Unlike BERT (400MB+), VADER is <1MB, runs instantly on a CPU, and requires no API keys. 
  - It is tuned for **social-media-style text and emojis**, which matches the “messy journaling” use case.  
  - It keeps the logic **transparent**: I can still see the raw scores and layer my own rules on top.

- **Hybrid logic – model + heuristics**  
  Instead of relying only on keywords or only on VADER, I combined both:
  - VADER provides a robust baseline sentiment score.  
  - Simple heuristics add an “energy index” (based on exclamation marks and ALL-CAPS words).  
  - A small rules layer corrects **ambiguous phrases** like:  
    - `"I am crushing it at work"` → Positive / high energy / **engaged**  
    - `"The workload is crushing me"` → Negative / high **stress**  
  This hybrid approach keeps the system **explainable** while still handling tricky language.

- **Storage format – JSON file**  
  I chose a local JSON file (`data/journal_entries.json`) instead of a database because:
  - The data volume for this challenge is small.  
  - JSON is **easy to inspect by eye**, which helps reviewers understand what the tool is doing.  
  - It avoids extra setup (no DB server or migrations) and keeps the focus on logic.

- **Interface – CLI only**  
  The prompt explicitly asks for a **Command-Line Interface**. I leaned into that by:
  - Keeping the CLI surface minimal (`add` and `summary` commands).  
  - Putting most of the complexity in the analyzer and storage modules, not the UI.  
  - Making the tool easy to script or extend later (e.g., more commands, different back-ends).

- **AI usage (high level)**  
  I used **GitHub Copilot** as a coding assistant to speed up boilerplate and explore options, but:
  - I wrote and organized the final modules myself.  
  - I added unit tests and manual CLI runs to verify behavior on edge cases.  
  - I treat all remaining bugs as my responsibility, not the model’s.

The rest of this README explains the project structure, how to run the CLI, the tagging logic, and a detailed **Methodology & AI Usage** section.

---

## 2. Project Structure

Key modules:

- ## src/analyzer.py  
  - WellbeingAnalyzer:
    - Uses vaderSentiment for base sentiment.  
    - Adds an “energy index” based on exclamation marks and ALL-CAPS words.  
    - Infers stress from mood + energy + explicit stress words.  
    - Adds override rules for phrases involving "crushing".

- ## src/storage.py  
  - JournalStorage handles JSON file I/O (data/journal_entries.json).  
  - Entry dataclass is the on-disk representation: id, created_at, text, tags, scores.

- ## src/cli.py  
  - add subcommand: analyze a new entry, persist it, print tags + scores.  
  - summary subcommand: print a formatted summary of the last N entries.

- ## tests/test_analyzer.py  
  - Unit tests for:
    - "crushing it" vs "crushing me".  
    - Empty input.  
    - Explicit stress words (e.g., "overwhelmed").  
    - High-energy text with ALL-CAPS and exclamation marks.

---

## 3. Setup and Installation

### 3.1 Prerequisites
* **Python 3.9+**
* A terminal (Bash/Zsh)

### 3.2 Installation
```bash
# 1. Clone the repository
git clone https://github.com/asogani23/panw_journal_challenge.git
cd panw_journal_challenge

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Make the helper script executable for Linux/Mac permissions (helpful, may not be required)
chmod +x run.sh
```
---

## 4. Usage

You can call the CLI with `python -m src.cli` or via the helper script `run.sh`.

### 4.1 Add an Entry

Using the helper script:

    ./run.sh add "I am absolutely CRUSHING IT at work today! 🔥"

Or directly via Python:

    python -m src.cli add "The workload is crushing me and I'm so stressed out..."

### 4.2 View Summary

    ./run.sh summary --last 3

### 4.3 Sample Output

    Last 3 entries from data/journal_entries.json:
    ========================================
    #4 @ 2025-12-07T04:03:36.658751+00:00
    I am absolutely CRUSHING IT at work today! 🔥
    Tags:
      - mood: positive
      - energy: medium
      - stress: engaged
    Scores:
      - energy_index: 0.25
      - sentiment (compound=-0.7366, pos=0.0, neu=0.53, neg=0.47)

Note on scores: in this example, the raw VADER score is negative because the lexicon treats “crushing” as destructive.  
My contextual logic layer recognizes the idiom "crushing it" and forces the tags to Positive / Engaged. I keep the raw scores so you can see the correction made by the heuristic layer.

You can also point the CLI at a custom storage file:

    ./run.sh --file data/alt_journal.json add "Separate test journal file."
    ./run.sh --file data/alt_journal.json summary --last 2
### 4.5 Running Tests

From the project root (after installing dependencies):

```bash
pytest
```

---

## 5. Tagging Logic (High Level)

For each entry, the WellbeingAnalyzer follows this pipeline:

1. Preprocessing  
   - Trim whitespace.  
   - If the result is empty → tags: mood=neutral, energy=low, stress=unknown.

2. Base Sentiment (VADER)  
   - Use SentimentIntensityAnalyzer to get compound, pos, neu, neg.  
   - Map compound to mood:
     - compound ≥ 0.4  → mood = "positive"  
     - compound ≤ -0.4 → mood = "negative"  
     - otherwise       → mood = "neutral"

3. Energy Calculation  
   - Count exclamation marks (!).  
   - Compute fraction of ALL-CAPS words (length > 2 and isupper()).  
   - Combine into an energy_index in [0, 1], then bucket:
     - energy_index < 0.3 → energy = "low"  
     - energy_index < 0.7 → energy = "medium"  
     - else               → energy = "high".

4. Stress Inference  
   - If the text contains words like "overwhelmed", "stressed", "anxious", "panic", "burned out" → stress = "high".  
   - Otherwise, use mood + energy:
     - mood = negative, energy = high   → stress = "high"  
     - mood = negative, energy = low    → stress = "drained"  
     - mood = positive, energy = high   → stress = "engaged"  
     - else                             → stress = "moderate".

5. Ambiguity Overrides for "crushing"  
   - If text contains "crushing it" or "crushing at":
     - Force mood = "positive", stress = "engaged", and avoid low energy.  
   - If text contains "crushing me" or "crushing my":
     - Force mood = "negative", stress = "high".  
     - If VADER’s compound was borderline (> -0.4), push it slightly negative.

This shows that the tool is not just doing a naive keyword search for "crushing"; it uses local context to resolve ambiguity.

---

## 6. Methodology & AI Usage

This section is explicit on purpose to follow the instructions about AI-native engineering.

### 6.1 Tools Used

- GitHub Copilot -
  I used Copilot as a coding assistant to:
  - Brainstorm the overall structure (splitting analyzer, storage, and cli).  
  - Draft the initial CLI.
  - Refine the phrasing in the README

- Local Python environment:
  - I installed and experimented with vaderSentiment.  
  - I ran the CLI with different sample entries.  
  - I tuned thresholds and overrides based on observed outputs.

### 6.2 How I Validated the Output of the tools I used

1. Unit Tests (tests/test_analyzer.py)

   I added tests to confirm that:

   - "I am absolutely CRUSHING IT at work today! 🔥"  
     → mood = positive, stress = engaged, energy is medium or high.  

   - "The workload is crushing me and I am so stressed out..."  
     → mood = negative, stress = high.  

   - Empty or whitespace-only text  
     → mood = neutral, energy = low, stress = unknown.  

   - Sentences containing "overwhelmed"  
     → stress = high.  

   - ALL-CAPS + "!!!" pushes energy toward medium/high.

2. Manual CLI Runs

   I used `./run.sh add ...` and `./run.sh summary --last N` with a variety of synthetic entries (positive, negative, neutral, high-energy, low-energy) to verify that:

   - The CLI does not crash on empty or messy input.  
   - data/journal_entries.json stays well-formed and readable.  
   - Tags behave as expected for ambiguous phrases like "crushing it" / "crushing me".

3. Threshold Tuning

   - Adjusted mood thresholds for VADER’s compound to reduce borderline mislabels.  
   - Tuned energy bucketing so casual messages do not show as “high energy,” but intense ALL-CAPS / punctuation does.

### 6.3 Ownership

Even though I used GitHub Copilot as a helper, I:

- Reviewed and edited every line of code.  
- Designed and refined the heuristics and override rules.  
- Wrote and ran the tests that gate the analyzer’s behavior.

I treat all bugs, edge cases, and security concerns in this repository as **my responsibility**, not the model’s.

---

## 7. Possible Extensions

If this were evolving into a real product or if I had more time, I would consider:

- Replacing VADER with a small transformer-based classifier fine-tuned on journaling data.  
- Adding a `trend` command to summarize mood and stress over time.  
- Supporting anonymized export of entries for further analysis or visual dashboards.  
- Growing the test suite to cover more regression cases as the heuristics evolve.

For this challenge, I focused on keeping the tool simple, robust, and easy to reason about, which lines up with the “Engineering Integrity” focus of the prompt.





 

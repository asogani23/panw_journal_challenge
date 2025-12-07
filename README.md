# AI-Powered Journaling CLI (PANW Intern Engineer Challenge)

Author: **Aagam Sogani**  
Role: Palo Alto Networks Product Software Engineer Intern Case Challenge  
Option: **1 – AI-Powered Journaling Logic**

---

## 1. Overview

This repo implements a small **command-line journaling tool** that analyzes raw, conversational text and tags each entry with mental well-being signals:

- `mood`   – positive / negative / neutral  
- `energy` – low / medium / high  
- `stress` – high / drained / engaged / moderate / unknown  

The goal is to demonstrate **AI-native engineering**:

- Handle “messy” text (slang, emojis, inconsistent grammar).  
- Use an NLP library for base sentiment instead of reinventing it.  
- Add contextual logic so:
  - "I am crushing it at work" → Positive / High energy / Engaged  
  - "The workload is crushing me" → Negative / High stress  
- Persist entries locally so the user can review their history.  
- Provide a simple CLI summary of the most recent entries.

---

## 2. Project Structure

Key modules:

- src/analyzer.py  
  - WellbeingAnalyzer:
    - Uses vaderSentiment for base sentiment.  
    - Adds an “energy index” based on exclamation marks and ALL-CAPS words.  
    - Infers stress from mood + energy + explicit stress words.  
    - Adds override rules for phrases involving "crushing".

- src/storage.py  
  - JournalStorage handles JSON file I/O (data/journal_entries.json).  
  - Entry dataclass is the on-disk representation: id, created_at, text, tags, scores.

- src/cli.py  
  - add subcommand: analyze a new entry, persist it, print tags + scores.  
  - summary subcommand: print a formatted summary of the last N entries.

- tests/test_analyzer.py  
  - Unit tests for:
    - "crushing it" vs "crushing me".  
    - Empty input.  
    - Explicit stress words (e.g., "overwhelmed").  
    - High-energy text with ALL-CAPS and exclamation marks.

---

## 3. Setup

Create and activate a virtual environment, then install dependencies:

    python -m venv venv
    source venv/bin/activate          # On Windows: venv\Scripts\activate
    pip install -r requirements.txt

This installs:

- vaderSentiment – sentiment analysis.  
- pytest – test runner.

Run the tests:

    pytest

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

- ChatGPT  
  I used ChatGPT as a coding assistant to:
  - Brainstorm the overall structure (splitting analyzer, storage, and cli).  
  - Iterate on the energy and stress heuristics.  
  - Draft the initial CLI and unit tests.

- Local Python environment  
  I:
  - Installed and experimented with vaderSentiment.  
  - Ran the CLI with different sample entries.  
  - Tuned thresholds and overrides based on observed outputs.

### 6.2 How I Validated the Output

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

### 6.3 Responsibility

Even though I used ChatGPT to speed up boilerplate and iterate on ideas, I:

- Reviewed and edited every line of code.  
- Designed and tuned the heuristics and override rules.  
- Wrote and ran tests to make sure the behavior matched the challenge spec.

I take responsibility for the final implementation and any remaining edge cases.

---

## 7. Possible Extensions

If this were evolving into a real product or if I had more time, I would consider:

- Replacing VADER with a small transformer-based classifier fine-tuned on journaling data.  
- Adding a `trend` command to summarize mood and stress over time.  
- Supporting anonymized export of entries for further analysis or visual dashboards.  
- Growing the test suite to cover more regression cases as the heuristics evolve.

For this challenge, I focused on keeping the tool simple, robust, and easy to reason about, which lines up with the “Engineering Integrity” focus of the prompt.





<pre> ## 6. Methodology & AI Usage This section follows the PANW guidelines on AI-native engineering, transparency, and verification. ### 6.1 Tools used - **ChatGPT** I used ChatGPT as a coding assistant to: - Brainstorm the module layout (`analyzer`, `storage`, `cli`, `tests`). - Iterate on the energy and stress heuristics. - Draft initial versions of the CLI and unit tests. - **Local Python environment** I: - Installed and experimented with `vaderSentiment`. - Ran the CLI with different sample entries. - Tuned thresholds and overrides based on the actual outputs. ### 6.2 How I verified the system 1. **Unit tests (`tests/test_analyzer.py`)** I added tests to confirm that: - `"I am absolutely CRUSHING IT at work today! 🔥"` → `mood = positive`, `stress = engaged`, `energy` is medium or high. - `"The workload is crushing me and I am so stressed out..."` → `mood = negative`, `stress = high`. - Empty or whitespace-only text → `mood = neutral`, `energy = low`, `stress = unknown`. - Sentences containing `"overwhelmed"` → `stress = high`. - ALL-CAPS text plus `!!!` shifts `energy` toward medium/high. 2. **Manual CLI runs** Using `./run.sh add ...` and `./run.sh summary --last N`, I checked that: - The CLI does not crash on messy input (slang, emojis, empty strings). - `data/journal_entries.json` stays well-formed and easy to read. - Tags behave as expected for ambiguous phrases like `"crushing it"` / `"crushing me"`. 3. **Threshold tuning** - Adjusted mood thresholds for VADER’s `compound` to reduce borderline mislabels. - Tuned energy bucketing so casual messages do not show as “high energy,” but intense ALL-CAPS / punctuation does. ### 6.3 Responsibility Even though I used ChatGPT to speed up some boilerplate and explore ideas, I: - Reviewed and edited every line of code. - Designed and refined the heuristics and override rules. - Wrote and ran tests to make sure the behavior matched the challenge spec. I take responsibility for the final implementation and any remaining edge cases or bugs. </pre>

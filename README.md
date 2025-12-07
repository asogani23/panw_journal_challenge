# AI-Powered Journaling CLI (PANW Intern Engineer Challenge)

**Author:** Aagam Sogani  
**Challenge:** Palo Alto Networks – Intern Engineer Case Challenge  
**Option:** Option 1 – AI-Powered Journaling Logic

---

## 📖 Overview

This repository implements a lightweight command-line journaling tool designed to analyze raw, conversational text and tag entries with mental well-being signals:

- **Mood:** `positive`, `negative`, `neutral`
- **Energy:** `low`, `medium`, `high`
- **Stress:** `high`, `drained`, `engaged`, `moderate`, `unknown`

The goal is to demonstrate **AI-native engineering** by orchestrating existing tools rather than reinventing them. The tool:

- Accepts “messy” input (slang, emojis, inconsistent grammar).
- Uses **VADER** (an NLP library) for base sentiment analysis.
- Implements a heuristic layer to handle linguistic ambiguity:
  - *"I am crushing it at work"* → **Positive / High Energy / Engaged**
  - *"The workload is crushing me"* → **Negative / High Stress**
- Persists entries to a local JSON file.
- Provides a CLI to log entries and view summaries.

---

## 📂 Project Structure

Key Modules
src/analyzer.py: The core logic. Uses vaderSentiment for base scores, then adds an "energy index" (based on caps/punctuation) and an override layer for context (e.g., "crushing").

src/storage.py: Handles safe JSON I/O, timestamping (UTC ISO 8601), and data integrity.

src/cli.py: The interface. Handles arguments for add and summary commands.

🚀 Setup and Usage
1. Install Dependencies
Bash

python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
pip install -r requirements.txt
2. Run Tests
I included a test suite to prove the logic handles the specific edge cases requested in the prompt.

Bash

pytest
Verifies: "Crushing it" (Positive) vs "Crushing me" (Negative), empty inputs, and explicit stress words.

3. Use the CLI
Add an Entry:

Bash

# Using the helper script
./run.sh add "I am absolutely CRUSHING IT at work today! 🔥"

# Or directly via Python
python -m src.cli add "The workload is crushing me and I'm so stressed out..."
View Summary:

Bash

./run.sh summary --last 3
Sample Output:

Plaintext

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
Note on Scores: In the example above, the raw VADER score (-0.7366) is negative because the lexicon interprets "crushing" as destructive. However, my Contextual Logic layer correctly identified the idiom "crushing it" and forced the tags to Positive/Engaged. I chose to preserve the raw score to visualize the "correction" made by the heuristic layer.

🧠 Tagging Logic (Methodology)
For each entry, the WellbeingAnalyzer follows this pipeline:

Preprocessing: Trims whitespace. Returns "Neutral/Low/Unknown" if empty.

Base Sentiment (VADER): Calculates a compound score.

>= 0.4: Positive

<= -0.4: Negative

Else: Neutral

Energy Calculation:

Counts exclamation marks (!).

Calculates fraction of ALL CAPS words.

Combines them into an energy_index (0.0 to 1.0).

Stress Inference:

Scans for explicit words: "overwhelmed", "panic", "burnout".

Derives state: Negative Mood + High Energy = High Stress.

Ambiguity Override (The "Human" Layer):

If text contains "crushing it": Force Mood=Positive, Stress=Engaged.

If text contains "crushing me": Force Mood=Negative, Stress=High.

🤖 AI Usage Disclosure
In compliance with the challenge rules regarding AI-Native Engineering:

Tools Used: ChatGPT (GPT-4o)

How I Used It:

Boilerplate: Generated the initial argparse skeleton and project structure to save setup time.

Ideation: Used as a sounding board to refine the "Energy Index" heuristic.

Data Generation: Generated synthetic test phrases (slang, emojis) to validate VADER's limits.

Verification & Ownership:

I manually wrote the Override Logic in analyzer.py to solve the specific "crushing" edge case.

I wrote the Unit Tests in tests/test_analyzer.py to mathematically prove the logic works.

I tuned the thresholds (e.g., 0.4 for sentiment) based on real CLI outputs.

I am fully responsible for every line of code in this repository.

🔮 Possible Extensions
If I were deploying this to production, I would:

Upgrade Model: Swap VADER for a lightweight Transformer (e.g., DistilBERT) fine-tuned on mental health texts for better context awareness without the need for manual overrides.

Trend Analysis: Add a trends command to visualize mood changes over time.

Data Privacy: Encrypt the JSON file at rest.

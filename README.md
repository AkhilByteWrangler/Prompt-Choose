# Prompt Selector

<p align="center">
  <a href="https://prompt-choose-production.up.railway.app/" target="_blank">
    <img src="https://img.shields.io/badge/Live%20Demo-prompt--choose-6B4FFF?style=for-the-badge" alt="Live Demo" />
  </a>
</p>

Collect human preference data on LLM responses. Django + MongoDB backend, React frontend.

## Features

- Generate two LLM responses with different parameters
- Compare and select preferences (A, B, or Tie)
- Export training data (prompt, chosen, rejected)
- Real-time statistics

## Stack

- Django, Django REST Framework, MongoDB, OpenAI API
- React, Vite, Framer Motion

## Prerequisites

- Python 3.8+, Node.js 16+, MongoDB, OpenAI API key

## Quick Start

```bash
./setup.sh
./start.sh
```

## Setup

**Backend**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create `.env`:
```
OPENAI_API_KEY=your_key
MONGODB_URI=mongodb://localhost:27017/
MONGODB_NAME=prompt_selector
```

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

- `POST /api/prompts/generate/` - Generate responses
- `POST /api/prompts/{id}/record-preference/` - Record preference
- `GET /api/prompts/export-training-data/` - Export data
- `GET /api/prompts/stats/` - Get stats

## Usage

1. Enter a prompt
2. Generate two responses
3. Select preference (A, B, or Tie)
4. Export training data

## Export Format

```json
{
  "prompt": "...",
  "chosen": "...",
  "rejected": "...",
  "metadata": {...}
}
```

## Dataset

A seed preference dataset is included in [`data/preference-dataset.json`](data/preference-dataset.json) — 15 labeled examples in the **high-stakes personal advice** category. Prompts are designed to make preference labeling non-trivial: neither response is objectively correct, and the signal comes from real value tradeoffs (autonomy vs. wellbeing, honesty vs. tact, caution vs. directness).

| # | Prompt | Preferred |
|---|--------|-----------|
| 1 | My doctor said my test results are "borderline" and wants to monitor for 6 months... | A |
| 2 | I've been offered a job that pays 40% more but requires relocating away from my aging parents... | A |
| 3 | My best friend told me in confidence that their partner cheated on them... | A |
| 4 | I've been sober for 2 years. My college reunion is next month... | A |
| 5 | I'm 28 and my parents keep pressuring me to have kids... | A |
| 6 | I found out my coworker is being paid $20k more than me for the same role... | A |
| 7 | My therapist suggested I try medication for anxiety. I'm resistant... | A |
| 8 | My startup is burning through runway and I've been offered an acquisition... | A |
| 9 | I ghosted a friend two years ago during a mental health crisis... | A |
| 10 | My partner wants to move in together after 8 months... | A |
| 11 | I've been caring for my sick parent for 3 years and I'm burning out... | A |
| 12 | I have a strong hunch my manager is going to lay off my team... | A |
| 13 | I've been offered a prestigious fellowship but it means deferring a relationship... | A |
| 14 | I suspect a colleague is inflating their expense reports... | A |
| 15 | I got a highly critical performance review that I think is partly motivated by bias... | A |

<details>
<summary>Dataset stats</summary>

- **Category:** High-stakes personal advice
- **Model:** gpt-3.5-turbo
- **Temperature A range:** 0.4 – 1.4
- **Temperature B range:** 0.5 – 1.2
- **Preference A:** 15 &nbsp;|&nbsp; **Preference B:** 0 &nbsp;|&nbsp; **Ties:** 0
- **Format:** `{ prompt, chosen, rejected, metadata }`

</details>

## License

MIT

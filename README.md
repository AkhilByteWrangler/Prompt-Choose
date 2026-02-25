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

## License

MIT

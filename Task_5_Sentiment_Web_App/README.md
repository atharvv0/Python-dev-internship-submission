# Task 5 — Sentiment Analysis Web Application

## Objective

Build a web application using Flask that accepts user-entered text and classifies it as **Positive**, **Negative**, or **Neutral** using TextBlob. The application also displays polarity and subjectivity scores.

## Technologies

- Python
- Flask
- TextBlob
- HTML5
- CSS3

## How to Run

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000` in a browser.

## Features

- Text input form
- Positive / Negative / Neutral classification
- Polarity score from TextBlob
- Subjectivity score from TextBlob
- Input validation for empty text
- Clean responsive interface

## Sample Test Inputs

- `I really enjoyed this internship and learned a lot.` → Positive
- `The application is slow and frustrating.` → Negative
- `The workshop starts at 10 AM tomorrow.` → Neutral

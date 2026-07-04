# 📝 Smart Note-Taking App with Analytics (Python + SQLite)

A full-featured command-line and GUI note-taking application with built-in analytics — tracking writing habits, tagging patterns, and note sentiment over time.

## 📌 Project Overview

This project goes beyond a basic notes app. It includes:
- Create, read, update, delete (CRUD) notes stored in SQLite
- Tag-based organisation and full-text search
- **Note analytics**: word count trends, most-used tags, writing frequency
- **Sentiment analysis** on note content (using TextBlob)
- Export notes to PDF or Markdown
- Automated daily backup

## 🛠️ Tools & Technologies
- Python 3.11
- SQLite (persistent storage)
- `tkinter` (GUI)
- `TextBlob` (sentiment analysis)
- `pandas` (analytics)
- `reportlab` (PDF export)

## 📁 Project Structure
```
07_note_taking_app/
├── src/
│   ├── notes_db.py            # SQLite CRUD operations
│   ├── analytics.py           # Usage & sentiment analytics
│   ├── search.py              # Full-text search engine
│   ├── export.py              # PDF & Markdown export
│   └── backup.py              # Automated backup module
├── gui/
│   └── app.py                 # tkinter desktop app
├── tests/
│   └── test_notes.py
├── data/
│   └── notes.db               # SQLite database
└── README.md
```

## 🔍 Sample Code — Notes CRUD
```python
import sqlite3
from datetime import datetime

def create_note(title: str, content: str, tags: list[str]) -> int:
    conn = sqlite3.connect('data/notes.db')
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO notes (title, content, tags, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, content, ','.join(tags), datetime.now(), datetime.now()))
    note_id = cur.lastrowid
    conn.commit()
    conn.close()
    return note_id

def search_notes(keyword: str) -> list:
    conn = sqlite3.connect('data/notes.db')
    df = pd.read_sql(
        "SELECT * FROM notes WHERE content LIKE ? OR title LIKE ?",
        conn, params=(f'%{keyword}%', f'%{keyword}%')
    )
    conn.close()
    return df.to_dict('records')
```

## 🔍 Analytics Feature
```python
from textblob import TextBlob
import pandas as pd

def analyse_sentiment(note_id: int) -> dict:
    note = get_note(note_id)
    blob = TextBlob(note['content'])
    return {
        'polarity':      round(blob.sentiment.polarity, 3),      # -1 to 1
        'subjectivity':  round(blob.sentiment.subjectivity, 3),  # 0 to 1
        'word_count':    len(note['content'].split()),
        'reading_time':  f"{len(note['content'].split()) // 200 + 1} min"
    }
```

## 📈 How to Run
```bash
pip install textblob pandas reportlab
python gui/app.py
```

---
*Part of Dhwani Shah's Data Analytics Portfolio*

"""
Note-Taking App with SQLite + Sentiment Analysis via Logistic Regression
Author: Dhwani Shah | Master of Business Analytics, Victoria University

Features:
  - SQLite-backed persistent note storage (CRUD)
  - Tag-based organisation
  - Search by keyword or tag
  - Sentiment classifier trained on synthetic labelled notes
  - Logistic Regression: predict note sentiment (Positive / Neutral / Negative)
"""
import sqlite3, os, re, json
import numpy as np
from datetime import datetime
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

BASE = os.path.dirname(os.path.abspath(__file__))
DB   = os.path.join(BASE, 'notes.db')

# ── Database setup ────────────────────────────────────────────────────────────
def get_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            content     TEXT NOT NULL,
            tags        TEXT DEFAULT '',
            created_at  TEXT DEFAULT (datetime('now','localtime')),
            updated_at  TEXT DEFAULT (datetime('now','localtime'))
        )
    """)
    conn.commit()
    return conn

def add_note(title, content, tags=""):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO notes (title, content, tags) VALUES (?, ?, ?)",
            (title, content, tags)
        )
        return cur.lastrowid

def get_note(note_id):
    with get_conn() as conn:
        return conn.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()

def list_notes(tag=None):
    with get_conn() as conn:
        if tag:
            return conn.execute("SELECT * FROM notes WHERE tags LIKE ?", (f'%{tag}%',)).fetchall()
        return conn.execute("SELECT * FROM notes ORDER BY created_at DESC").fetchall()

def update_note(note_id, title=None, content=None, tags=None):
    with get_conn() as conn:
        note = conn.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
        if not note:
            raise ValueError(f"Note {note_id} not found.")
        conn.execute("""
            UPDATE notes SET title=?, content=?, tags=?, updated_at=datetime('now','localtime')
            WHERE id=?
        """, (title or note['title'], content or note['content'],
              tags if tags is not None else note['tags'], note_id))

def delete_note(note_id):
    with get_conn() as conn:
        conn.execute("DELETE FROM notes WHERE id=?", (note_id,))

def search_notes(keyword):
    kw = f'%{keyword}%'
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM notes WHERE title LIKE ? OR content LIKE ? OR tags LIKE ?",
            (kw, kw, kw)
        ).fetchall()

# ── Sentiment Model ───────────────────────────────────────────────────────────
TRAINING_DATA = [
    ("Great meeting today! Team was enthusiastic and results exceeded expectations.", "Positive"),
    ("Completed all tasks ahead of schedule. Very productive session.", "Positive"),
    ("The project is going well. Client is happy with our progress.", "Positive"),
    ("Excellent analysis — leadership praised the dashboard work.", "Positive"),
    ("System working smoothly. All KPIs are on track.", "Positive"),
    ("Team morale is high. Delivered the report on time.", "Positive"),
    ("Meeting scheduled for 3pm. Agenda includes project review.", "Neutral"),
    ("Reviewed the data and updated the spreadsheet.", "Neutral"),
    ("Need to follow up with supplier about lead times.", "Neutral"),
    ("Data exported to CSV. Will process tomorrow.", "Neutral"),
    ("Called the client. Will get back to us by end of week.", "Neutral"),
    ("Updated the README file and pushed the changes.", "Neutral"),
    ("Delayed again. The supplier failed to deliver on time.", "Negative"),
    ("Report has errors. KPIs are not matching expectations.", "Negative"),
    ("High defect rate this week. Quality is a major concern.", "Negative"),
    ("Meeting was unproductive. No decisions made.", "Negative"),
    ("Data is missing for three months — significant gap in analysis.", "Negative"),
    ("Client is unhappy with the turnaround time. Need urgent fix.", "Negative"),
]

def train_sentiment_model():
    from sklearn.model_selection import cross_val_score
    texts  = [t for t, _ in TRAINING_DATA]
    labels = [l for _, l in TRAINING_DATA]
    vec = TfidfVectorizer(max_features=200, stop_words='english', ngram_range=(1,2))
    X   = vec.fit_transform(texts)
    y   = np.array(labels)
    clf = LogisticRegression(max_iter=300, random_state=42, C=0.5)
    cv_scores = cross_val_score(clf, X, y, cv=6, scoring='accuracy')
    clf.fit(X, y)
    acc = cv_scores.mean()
    return vec, clf, acc

def predict_sentiment(text, vec, clf):
    X = vec.transform([text])
    pred  = clf.predict(X)[0]
    proba = clf.predict_proba(X)[0]
    conf  = max(proba)
    return pred, conf

# ── Demo ──────────────────────────────────────────────────────────────────────
def run_demo():
    # Clear old DB for clean demo
    if os.path.exists(DB):
        os.remove(DB)

    print("\n" + "="*60)
    print("  NOTE-TAKING APP — DEMO")
    print("="*60)

    # Add sample notes
    n1 = add_note("Supply Chain Review",
                  "Completed supplier performance analysis. Aussie Meats leads at 89% OTD. GrocerPlus flagged for review.",
                  tags="supply-chain,performance")
    n2 = add_note("Data Pipeline Issue",
                  "Missing data for weeks 23-26. Defect rate spiked. Need to investigate cold-chain protocols urgently.",
                  tags="pipeline,data-quality,urgent")
    n3 = add_note("Client Meeting Notes",
                  "Met with client team. They appreciated the RFM dashboard. Next steps: monthly automated report.",
                  tags="client,meeting,rfm")
    n4 = add_note("Weekly KPI Summary",
                  "On-time delivery rate: 77%. Defect rate: 4.8%. Lead time avg: 2.9 days. All within acceptable range.",
                  tags="kpi,weekly")

    print(f"\n  Created 4 notes.\n")

    # List all
    notes = list_notes()
    print(f"  All Notes ({len(notes)} total):")
    for n in notes:
        print(f"    [{n['id']}] {n['title']}  |  tags: {n['tags']}")

    # Search
    results = search_notes("defect")
    print(f"\n  Search 'defect' → {len(results)} result(s):")
    for r in results:
        print(f"    [{r['id']}] {r['title']}")

    # Update
    update_note(n1, content="UPDATED: Supplier review complete. GrocerPlus placed on 30-day improvement plan.")
    print(f"\n  Updated note {n1}.")

    # Delete
    delete_note(n4)
    print(f"  Deleted note {n4}.")

    # Remaining
    notes = list_notes()
    print(f"\n  Notes remaining: {len(notes)}")

    # Sentiment Analysis
    print(f"\n  {'─'*60}")
    print("  LOGISTIC REGRESSION — Sentiment Classifier")
    vec, clf, acc = train_sentiment_model()
    print(f"  Training accuracy : {acc*100:.1f}% on held-out set")
    print(f"\n  Sentiment Predictions:")
    for n in notes:
        sentiment, conf = predict_sentiment(n['content'], vec, clf)
        emoji = "✅" if sentiment=="Positive" else ("⚠️" if sentiment=="Neutral" else "❌")
        print(f"    {emoji} [{n['id']}] {n['title'][:40]:<40} → {sentiment} ({conf*100:.0f}% conf.)")

    print(f"\n  {'─'*60}")
    print("  Tag-based Filter (tag='supply-chain'):")
    tagged = list_notes(tag='supply-chain')
    for n in tagged:
        print(f"    [{n['id']}] {n['title']}")

    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    run_demo()

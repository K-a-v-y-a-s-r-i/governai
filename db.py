"""GovernAI storage: every judged pair is saved under its model name in SQLite."""
import sqlite3
from pathlib import Path
import os, sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "data")          # adjust if you use a different folder
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "governai.db")    # use your real filename

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
DB_PATH = Path(__file__).with_name("governai.db")

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
conn.execute(
    """CREATE TABLE IF NOT EXISTS judgments (
        id INTEGER PRIMARY KEY,
        model TEXT, prompt TEXT, response TEXT,
        category TEXT, expected TEXT, actual TEXT,
        pass INTEGER, severity TEXT, reason TEXT,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""
)
conn.commit()


def save(model: str, prompt: str, response: str, j: dict) -> None:
    conn.execute(
        """INSERT INTO judgments
           (model, prompt, response, category, expected, actual, pass, severity, reason)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (model, prompt, response, j["category"], j["expected"], j["actual"],
         int(j["pass"]), j["severity"], j["reason"]),
    )
    conn.commit()


def load(model: str) -> list[dict]:
    rows = conn.execute(
        """SELECT prompt, response, category, pass, severity, reason, actual
           FROM judgments WHERE model = ? ORDER BY id""",
        (model,),
    ).fetchall()
    return [
        {"prompt": r[0], "response": r[1], "category": r[2], "pass": bool(r[3]),
         "severity": r[4], "reason": r[5], "actual": r[6]}
        for r in rows
    ]


def models_with_data() -> list[str]:
    return [r[0] for r in conn.execute("SELECT DISTINCT model FROM judgments ORDER BY model")]


def clear(model: str | None = None) -> None:
    """Delete stored judgments for one model, or everything if model is None."""
    if model:
        conn.execute("DELETE FROM judgments WHERE model = ?", (model,))
    else:
        conn.execute("DELETE FROM judgments")
    conn.commit()

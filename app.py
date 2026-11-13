import os
import sqlite3
from contextlib import closing
from pathlib import Path

from flask import Flask, jsonify, request


def create_app(database_path=None):
    app = Flask(__name__)
    database = Path(database_path or os.environ.get("DATABASE_PATH", "data/message.db"))
    database.parent.mkdir(parents=True, exist_ok=True)

    with closing(sqlite3.connect(database)) as connection:
        connection.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, message TEXT NOT NULL)")
        connection.execute("INSERT OR IGNORE INTO messages VALUES (1, ?)", ("Hello World",))
        connection.commit()

    @app.get("/api/message")
    def get_message():
        with closing(sqlite3.connect(database)) as connection:
            row = connection.execute("SELECT message FROM messages WHERE id = 1").fetchone()
        return jsonify(message=row[0])

    @app.put("/api/message")
    def update_message():
        data = request.get_json(silent=True)
        message = data.get("message") if isinstance(data, dict) else None
        if not isinstance(message, str) or not 1 <= len(message.strip()) <= 200:
            return jsonify(error="Enter a message between 1 and 200 characters."), 400

        message = message.strip()
        with closing(sqlite3.connect(database)) as connection:
            connection.execute("UPDATE messages SET message = ? WHERE id = 1", (message,))
            connection.commit()
        return jsonify(message=message)

    return app


if __name__ == "__main__":
    create_app().run(host=os.environ.get("HOST", "127.0.0.1"), port=5000)

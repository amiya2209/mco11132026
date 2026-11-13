import sqlite3
import tempfile
import unittest

from contextlib import closing
from pathlib import Path

from app import create_app


class MessageTests(unittest.TestCase):
    def test_read_update_and_persistence(self):
        with tempfile.TemporaryDirectory() as folder:
            database = Path(folder) / "test.db"
            client = create_app(database).test_client()
            self.assertEqual(client.get("/api/message").json, {"message": "Hello World"})

            response = client.put("/api/message", json={"message": "Updated message"})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"message": "Updated message"})

            with closing(sqlite3.connect(database)) as connection:
                row = connection.execute("SELECT message FROM messages WHERE id = 1").fetchone()
            self.assertEqual(row[0], "Updated message")

            new_client = create_app(database).test_client()
            self.assertEqual(new_client.get("/api/message").json["message"], "Updated message")

    def test_invalid_message(self):
        with tempfile.TemporaryDirectory() as folder:
            client = create_app(Path(folder) / "test.db").test_client()
            for message in ["", "   ", "x" * 201, 123]:
                response = client.put("/api/message", json={"message": message})
                self.assertEqual(response.status_code, 400)
            self.assertEqual(client.get("/api/message").json["message"], "Hello World")


if __name__ == "__main__":
    unittest.main()

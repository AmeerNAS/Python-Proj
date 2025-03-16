import unittest
import os
import json
from datetime import datetime
from app.db import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        """Creates a temporary database file for testing."""
        self.test_db_file = "test_db.json"
        self.db = Database(self.test_db_file)
        self.db.db = {  # Reset database to a known state
            "database": self.test_db_file,
            "tables": {"habit": [], "history": []}
        }
        self.db.saveDB()

    def tearDown(self):
        """Removes the temporary database file after tests."""
        if os.path.exists(self.test_db_file):
            os.remove(self.test_db_file)

    def test_addHabit(self):
        """Tests adding a new habit."""
        habit_id = self.db.addHabit("Exercise", "Morning workout", "DAILY")
        habit = self.db.getHabitByID(habit_id)
        self.assertIsNotNone(habit)
        self.assertEqual(habit["name"], "Exercise")
        self.assertEqual(habit["interval"], "DAILY")

    def test_addHabit_duplicate(self):
        """Tests that adding a duplicate habit raises an error."""
        self.db.addHabit("Read", "Read a book", "DAILY")
        with self.assertRaises(ValueError):
            self.db.addHabit("Read", "Read a book", "DAILY")

    def test_addHistory(self):
        """Tests adding history for a habit."""
        habit_id = self.db.addHabit("Meditation", "Daily meditation", "DAILY")
        result = self.db.addHistory(habit_id, 3, "active", "2025-03-16")
        self.assertTrue(result)
        history = [h for h in self.db.db["tables"]["history"] if h["habit_id"] == habit_id]
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["status"], "active")

    def test_deleteHabit(self):
        """Tests deleting a habit and its history."""
        habit_id = self.db.addHabit("Jogging", "Evening jog", "WEEKLY")
        self.db.addHistory(habit_id, 5, "active", "2025-03-10")
        result = self.db.deleteHabit(habit_id)
        self.assertTrue(result)
        self.assertIsNone(self.db.getHabitByID(habit_id))
        self.assertEqual(len(self.db.db["tables"]["history"]), 0)

    def test_updateHabit(self):
        """Tests updating a habit's details."""
        habit_id = self.db.addHabit("Yoga", "Morning yoga", "DAILY")
        self.db.updateHabit(habit_id, name="Evening Yoga", desc="Relaxing yoga session")
        habit = self.db.getHabitByID(habit_id)
        self.assertEqual(habit["name"], "Evening Yoga")
        self.assertEqual(habit["desc"], "Relaxing yoga session")

    def test_updateHistory(self):
        """Tests updating a habit's history."""
        habit_id = self.db.addHabit("Coding", "Practice coding", "DAILY")
        self.db.addHistory(habit_id, 2, "active", "2025-03-14")
        self.db.updateHistory(habit_id, "2025-03-14", 3, "active")
        history = [h for h in self.db.db["tables"]["history"] if h["habit_id"] == habit_id]
        self.assertEqual(history[0]["streak"], 3)

if __name__ == "__main__":
    unittest.main()

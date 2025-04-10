# Simple in-memory database for user points


from typing import Dict

# In-memory storage for user points
# Format: {user_id: points}
user_points_db: Dict[str, int] = {}

def get_user_points(user_id: str) -> int:
    """
    Get the current points for a user.
    
    Args:
        user_id: The user's unique identifier
        
    Returns:
        The user's current points (0 if user not found)
    """
    return user_points_db.get(user_id, 0)

def update_user_points(user_id: str, points: int) -> None:
    """
    Update the points for a user.
    
    Args:
        user_id: The user's unique identifier
        points: The new total points value
    """
    user_points_db[user_id] = points

# For a real database implementation, you might have code like this:
'''
import sqlite3
from contextlib import contextmanager

DATABASE_PATH = "recycling_rewards.db"

def init_db():
    """Initialize the database with necessary tables."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                points INTEGER DEFAULT 0
            )
        """)
        conn.commit()

@contextmanager
def get_db_connection():
    """Context manager for database connections."""
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        yield conn
    finally:
        conn.close()

def get_user_points(user_id: str) -> int:
    """Get points for a user."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT points FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        return result[0] if result else 0

def update_user_points(user_id: str, points: int) -> None:
    """Update points for a user."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (id, points) VALUES (?, ?)
            ON CONFLICT (id) DO UPDATE SET points = ?
        """, (user_id, points, points))
        conn.commit()

# Initialize the database when this module is imported
init_db()
'''
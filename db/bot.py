import sqlite3
import logging

# Set up logging for database operations
logger = logging.getLogger(__name__)

DATABASE_NAME = 'bot.db'

def get_db_connection():
    """Helper function to get a database connection."""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        return conn
    except sqlite3.Error as e:
        logger.error(f"❌ Database connection error: {e}")
        raise

def init_db():
    """Initialize the database and create necessary tables if they don't exist."""
    try:
        conn = get_db_connection()
        with conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS log_channels (
                            guild_id INTEGER PRIMARY KEY,
                            channel_id INTEGER
                        )''')
            c.execute('''CREATE TABLE IF NOT EXISTS warnings (
                            user_id INTEGER,
                            guild_id INTEGER,
                            reason TEXT,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                        )''')
            logger.info("✅ Database initialized and tables created if not existing.")
    except sqlite3.Error as e:
        logger.error(f"❌ Error initializing the database: {e}")

def set_log_channel(guild_id, channel_id):
    """Sets the log channel for a specific guild."""
    try:
        conn = get_db_connection()
        with conn:
            c = conn.cursor()
            c.execute('REPLACE INTO log_channels (guild_id, channel_id) VALUES (?, ?)', (guild_id, channel_id))
            logger.info(f"✅ Log channel set for guild {guild_id} to {channel_id}.")
    except sqlite3.Error as e:
        logger.error(f"❌ Error setting log channel for guild {guild_id}: {e}")

def get_log_channel(guild_id):
    """Retrieves the log channel for a specific guild."""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT channel_id FROM log_channels WHERE guild_id = ?', (guild_id,))
        result = c.fetchone()
        if result:
            logger.info(f"✅ Retrieved log channel for guild {guild_id}: {result[0]}")
            return result[0]
        else:
            logger.warning(f"⚠️ No log channel set for guild {guild_id}.")
            return None
    except sqlite3.Error as e:
        logger.error(f"❌ Error retrieving log channel for guild {guild_id}: {e}")
        return None

def add_warning(user_id, guild_id, reason):
    """Adds a warning for a user in a specific guild."""
    try:
        conn = get_db_connection()
        with conn:
            c = conn.cursor()
            c.execute('INSERT INTO warnings (user_id, guild_id, reason) VALUES (?, ?, ?)', (user_id, guild_id, reason))
            logger.info(f"✅ Warning added for user {user_id} in guild {guild_id}. Reason: {reason}")
    except sqlite3.Error as e:
        logger.error(f"❌ Error adding warning for user {user_id} in guild {guild_id}: {e}")

def get_warnings(user_id, guild_id):
    """Retrieves all warnings for a specific user in a specific guild."""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT reason, timestamp FROM warnings WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
        results = c.fetchall()
        if results:
            logger.info(f"✅ Retrieved {len(results)} warnings for user {user_id} in guild {guild_id}.")
        else:
            logger.warning(f"⚠️ No warnings found for user {user_id} in guild {guild_id}.")
        return results
    except sqlite3.Error as e:
        logger.error(f"❌ Error retrieving warnings for user {user_id} in guild {guild_id}: {e}")
        return []


